import os
import copy
import json
import os.path
import random

import torch
import pytorch_lightning as pl
from PIL import Image
from tqdm import tqdm
from torch.utils.data import DataLoader
from transformers import CLIPProcessor
from urllib.parse import unquote

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def _load_json_file(filepath):
    data = []
    if isinstance(filepath, str):
        with open(filepath, 'r', encoding='utf-8') as f:
            d = json.load(f)
            data.extend(d)
    elif isinstance(filepath, list):
        for path in filepath:
            with open(path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                data.extend(d)
    return data


class DataModuleForMIMIC(pl.LightningDataModule):
    def __init__(self, args):
        super(DataModuleForMIMIC, self).__init__()
        self.args = args
        self.tokenizer = CLIPProcessor.from_pretrained(self.args.pretrained_model).tokenizer
        self.image_processor = CLIPProcessor.from_pretrained(self.args.pretrained_model).feature_extractor
        with open(self.args.data.qid2id, 'r', encoding='utf-8') as f:
            self.qid2id = json.loads(f.readline())
        self.raw_kb_entity = sorted(_load_json_file(self.args.data.entity), key=lambda x: x['id'])
        self.kb_entity = self.setup_dataset_for_entity(self.raw_kb_entity)
        self.kb_id2entity = {raw_ent['id']: ent for raw_ent, ent in zip(self.raw_kb_entity, self.kb_entity)}

        train_data = _load_json_file(self.args.data.train_file)
        self.train_data = self.setup_dataset_for_mention(train_data)
        self.val_data = self.setup_dataset_for_mention(_load_json_file(self.args.data.dev_file))
        self.test_data = self.setup_dataset_for_mention(_load_json_file(self.args.data.test_file))

    def setup_dataset_for_entity(self, data):
        # prepare entity information
        input_data = []
        for sample_dict in tqdm(data, desc='PreProcessing'):
            sample_type = sample_dict['type']
            if sample_type == 'entity':
                entity, attr = unquote(sample_dict.pop('entity_name')), sample_dict.pop('attr')
                input_text = entity + ' [SEP] ' + attr  # concat entity and sentence
                input_dict = self.tokenizer(input_text, padding='max_length', max_length=self.args.data.text_max_length,
                                            truncation=True)
            input_dict['img_list'] = sample_dict['image_list']
            input_dict['sample_type'] = 0 if sample_type == 'entity' else 1
            if 'answer' in sample_dict.keys():
                input_dict['answer'] = self.qid2id[sample_dict['answer']]
            input_data.append(input_dict)
        return input_data

    def setup_dataset_for_mention(self, data):
        # prepare mention information
        input_data = []
        for sample_dict in tqdm(data, desc='PreProcessing'):
            sample_type = 1
            mention, text = unquote(sample_dict.pop('mentions')), sample_dict.pop('sentence')
            input_text = mention + ' [SEP] ' + text  # concat entity and text
            input_dict = self.tokenizer(input_text, padding='max_length', max_length=self.args.data.text_max_length,
                                        truncation=True)

            input_dict['img_list'] = [sample_dict['imgPath']] if sample_dict['imgPath'] != '' else []
            input_dict['sample_type'] = sample_type

            if 'answer' in sample_dict.keys():
                input_dict['answer'] = self.qid2id[sample_dict['answer']]
            if sample_dict['answer'] == 'nil':  # ignore the sample without ground truth
                continue
            input_data.append(input_dict)
        return input_data


    def choose_image(self, sample_type, img_list, is_eval=False):
        if len(img_list):
            img_name = random.choice(img_list)
            # when evaluation, we choose the first image
            if is_eval:
                img_name = img_list[0]
            if sample_type == 1:
                img_name = img_name.split('/')[-1].split('.')[0] + '.jpg'   # we already convert all image to jpg format
            try:
                img_path = os.path.join(
                    self.args.data.kb_img_folder if sample_type == 0 else self.args.data.mention_img_folder,
                    img_name)
                img = Image.open(img_path).resize((224, 224), Image.Resampling.LANCZOS)
                pixel_values = self.image_processor(img, return_tensors='pt')['pixel_values'].squeeze()
            except:
                pixel_values = torch.zeros((3, 224, 224))
        else:
            pixel_values = torch.zeros((3, 224, 224))
        return pixel_values

    def train_collator(self, samples):
        cls_idx, img_list, sample_type, input_dict_list = [], [], [], []
        pixel_values, gt_ent_id = [], []

        # collect the metadata that need to further process
        for sample_idx, sample in enumerate(samples):
            img_list.append(sample.pop('img_list'))         # mention image list
            sample_type.append(sample.pop('sample_type'))   # input type: 0 for mention and 1 for entity
            input_dict_list.append(sample)                  # mention input dict (input_tokens, token_type_ids, attention_mask)
            gt_ent_id.append(sample.pop('answer'))          # ground truth entity id of mentions
        ###
        # Now we process mention information
        # choose an image
        for idx, _ in enumerate(input_dict_list):
            pixel_values.append(self.choose_image(sample_type[idx], img_list[idx]))
        # pad textual input
        input_dict = self.tokenizer.pad(input_dict_list,
                                        padding='max_length',
                                        max_length=self.args.data.text_max_length,
                                        return_tensors='pt')
        # concat all images
        pixel_values = torch.stack(pixel_values)
        input_dict['pixel_values'] = pixel_values

        ###
        # now we process entity information
        # fetch the entities' metadata
        ent_info_list = [copy.deepcopy(self.kb_id2entity[idx]) for idx in gt_ent_id]
        ent_img_list, ent_type, ent_input_dict_list, ent_pixel_values = [], [], [], []
        for ent_dict in ent_info_list:
            ent_img_list.append(ent_dict.pop('img_list'))   # entity image list
            ent_type.append(ent_dict.pop('sample_type'))    # input type: 0 for mention and 1 for entity
            ent_input_dict_list.append(ent_dict)            # entity input dict (input_tokens, token_type_ids, attention_mask)
        # choose an image
        for idx, _ in enumerate(ent_input_dict_list):
            ent_pixel_values.append(self.choose_image(ent_type[idx], ent_img_list[idx]))
        # some of the entities do not have image, so we use bool flags to tag them
        ent_empty_img_flag = torch.tensor([True if not len(_) else False for _ in ent_img_list], dtype=torch.bool)
        # pad textual input
        ent_input_dict = self.tokenizer.pad(ent_input_dict_list,
                                            padding='max_length',
                                            max_length=self.args.data.text_max_length,
                                            return_tensors='pt')
        # concat all image
        ent_pixel_values = torch.stack(ent_pixel_values)
        ent_input_dict['pixel_values'] = ent_pixel_values
        ent_input_dict['empty_img_flag'] = ent_empty_img_flag

        # for the entity information, we use prefix 'ent_' to tag them
        for k, v in ent_input_dict.items():
            input_dict[f'ent_{k}'] = v
        return input_dict

    def eval_collator(self, samples):
        # eval collator is similar to train collator, but only include mention information
        cls_idx, img_list, sample_type, input_dict_list = [], [], [], []
        pixel_values, gt_ent_id = [], []

        for sample_idx, sample in enumerate(samples):
            img_list.append(sample.pop('img_list'))
            sample_type.append(sample.pop('sample_type'))
            gt_ent_id.append(sample.pop('answer'))
            input_dict_list.append(sample)

        for idx, _ in enumerate(input_dict_list):
            pixel_values.append(self.choose_image(sample_type[idx], img_list[idx], is_eval=True))

        input_dict = self.tokenizer.pad(input_dict_list,
                                        padding='max_length',
                                        max_length=self.args.data.text_max_length,
                                        return_tensors='pt')
        input_dict['pixel_values'] = torch.stack(pixel_values)
        input_dict['answer'] = torch.tensor(gt_ent_id, dtype=torch.long)
        return input_dict

    def entity_collator(self, samples):
        # entity collator is similar to train collator, but only include entity information
        pixel_values, img_list, sample_type, input_dict_list = [], [], [], []
        for sample_idx, sample in enumerate(samples):
            img_list.append(sample.pop('img_list'))
            sample_type.append(sample.pop('sample_type'))
            input_dict_list.append(sample)
        for idx, input_dict in enumerate(input_dict_list):
            pixel_values.append(self.choose_image(sample_type[idx], img_list[idx], is_eval=True))

        input_dict = self.tokenizer.pad(input_dict_list,
                                        padding='max_length',
                                        max_length=self.args.data.text_max_length,
                                        return_tensors='pt')
        input_dict['pixel_values'] = torch.stack(pixel_values)

        return input_dict

    def entity_dataloader(self):
        return DataLoader(self.kb_entity,
                          batch_size=self.args.data.embed_update_batch_size,
                          num_workers=self.args.data.num_workers,
                          shuffle=False,
                          collate_fn=self.entity_collator)

    def train_dataloader(self):
        return DataLoader(self.train_data,
                          batch_size=self.args.data.batch_size,
                          num_workers=self.args.data.num_workers,
                          shuffle=True,
                          collate_fn=self.train_collator)

    def val_dataloader(self):
        return DataLoader(self.val_data,
                          batch_size=self.args.data.eval_batch_size,
                          num_workers=self.args.data.num_workers,
                          shuffle=False,
                          collate_fn=self.eval_collator)

    def test_dataloader(self):
        return DataLoader(self.test_data,
                          batch_size=self.args.data.eval_batch_size,
                          num_workers=self.args.data.num_workers,
                          shuffle=False,
                          collate_fn=self.eval_collator)
