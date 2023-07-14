import json
import os
import time
import math
import numpy as np
import torch
import pytorch_lightning as pl
from tqdm import tqdm
from codes.model.modeling_mimic import MIMICEncoder, MIMICMatcher


class LightningForMIMIC(pl.LightningModule):
    def __init__(self, args):
        super(LightningForMIMIC, self).__init__()
        self.args = args
        self.save_hyperparameters(args)

        self.encoder = MIMICEncoder(args)
        self.matcher = MIMICMatcher(args)
        self.loss_fct = torch.nn.CrossEntropyLoss()

    def training_step(self, batch):
        ent_batch = {}
        mention_batch = {}
        for k, v in batch.items():
            if k.startswith('ent_'):
                ent_batch[k.replace('ent_', '')] = v
            else:
                mention_batch[k] = v
        entity_empty_image_flag = ent_batch.pop('empty_img_flag')   # not use

        # [bs, dim]
        mention_text_embeds, mention_image_embeds, mention_text_seq_tokens, mention_image_patch_tokens = \
            self.encoder(**mention_batch)
        entity_text_embeds, entity_image_embeds, entity_text_seq_tokens, entity_image_patch_tokens = \
            self.encoder(**ent_batch)
        logits, (text_logits, image_logits, image_text_logits) = self.matcher(entity_text_embeds,
                                                                              entity_text_seq_tokens,
                                                                              mention_text_embeds,
                                                                              mention_text_seq_tokens,
                                                                              entity_image_embeds,
                                                                              entity_image_patch_tokens,
                                                                              mention_image_embeds,
                                                                              mention_image_patch_tokens)
        labels = torch.arange(len(mention_text_embeds)).long().to(mention_text_embeds.device)

        text_loss = self.loss_fct(text_logits, labels)
        image_loss = self.loss_fct(image_logits, labels)
        image_text_loss = self.loss_fct(image_text_logits, labels)
        overall_loss = self.loss_fct(logits, labels)

        loss = overall_loss + text_loss + image_loss + image_text_loss
        self.log('Train/loss', loss.detach().cpu().item(), on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        answer = batch.pop('answer')
        batch_size = len(answer)
        mention_text_embeds, mention_image_embeds, mention_text_seq_tokens, mention_image_patch_tokens = \
            self.encoder(**batch)  # [bs, dim]

        # We use chuck/mini-batch to alleviate GRAM usage
        scores = []
        chunk_size = self.args.data.eval_chunk_size
        for idx in range(math.ceil(self.args.data.num_entity / chunk_size)):
            start_pos = idx * chunk_size
            end_pos = (idx + 1) * chunk_size

            chunk_entity_text_embeds = self.entity_text_embeds[start_pos:end_pos].to(mention_text_embeds.device)
            chunk_entity_image_embeds = self.entity_image_embeds[start_pos:end_pos].to(mention_text_embeds.device)
            chunk_entity_text_seq_tokens = self.entity_text_seq_tokens[start_pos:end_pos].to(mention_text_embeds.device)
            chunk_entity_image_patch_tokens = self.entity_image_patch_tokens[start_pos:end_pos].to(
                mention_text_embeds.device)

            chunk_score, _ = self.matcher(chunk_entity_text_embeds, chunk_entity_text_seq_tokens,
                                          mention_text_embeds, mention_text_seq_tokens,
                                          chunk_entity_image_embeds, chunk_entity_image_patch_tokens,
                                          mention_image_embeds, mention_image_patch_tokens)
            scores.append(chunk_score)

        scores = torch.concat(scores, dim=-1)
        rank = torch.argsort(torch.argsort(scores, dim=-1, descending=True), dim=-1, descending=False) + 1
        tgt_rank = rank[torch.arange(batch_size), answer].detach().cpu()
        return dict(rank=tgt_rank, all_rank=rank.detach().cpu().numpy())

    def on_validation_start(self):
        # Update entity embedding before validation starts
        # Note that we use entity_dataloader defined in our datamodule (please see codes/utils/dataset)
        entity_dataloader = self.trainer.datamodule.entity_dataloader()
        outputs_text_embed = []
        outputs_image_embed = []
        outputs_text_seq_tokens = []
        outputs_image_patch_tokens = []

        with torch.no_grad():
            for batch in tqdm(entity_dataloader, desc='UpdateEmbed', total=len(entity_dataloader)):
                batch = pl.utilities.move_data_to_device(batch, self.device)
                entity_text_embeds, entity_image_embeds, entity_text_seq_tokens, entity_image_patch_tokens = \
                    self.encoder(**batch)
                outputs_text_embed.append(entity_text_embeds.cpu())
                outputs_image_embed.append(entity_image_embeds.cpu())
                outputs_text_seq_tokens.append(entity_text_seq_tokens.cpu())
                outputs_image_patch_tokens.append(entity_image_patch_tokens.cpu())

        self.entity_text_embeds = torch.concat(outputs_text_embed, dim=0)
        self.entity_image_embeds = torch.concat(outputs_image_embed, dim=0)
        self.entity_text_seq_tokens = torch.concat(outputs_text_seq_tokens, dim=0)
        self.entity_image_patch_tokens = torch.concat(outputs_image_patch_tokens, dim=0)

    def validation_epoch_end(self, outputs):
        self.entity_text_embeds = None
        self.entity_image_embeds = None
        self.entity_text_seq_tokens = None
        self.entity_image_patch_tokens = None

        ranks = np.concatenate([_['rank'] for _ in outputs])
        hits20 = (ranks <= 20).mean()
        hits10 = (ranks <= 10).mean()
        hits5 = (ranks <= 5).mean()
        hits3 = (ranks <= 3).mean()
        hits1 = (ranks <= 1).mean()

        self.log("Val/hits20", hits20)
        self.log("Val/hits10", hits10)
        self.log("Val/hits5", hits5)
        self.log("Val/hits3", hits3)
        self.log("Val/hits1", hits1)
        self.log("Val/mr", ranks.mean())
        self.log("Val/mrr", (1. / ranks).mean())

    def test_step(self, batch, batch_idx, dataloader_idx=None):
        answer = batch.pop('answer')
        batch_size = len(answer)
        mention_text_embeds, mention_image_embeds, mention_text_seq_tokens, mention_image_patch_tokens = \
            self.encoder(**batch)  # bs, dim

        # We use chuck/mini-batch to alleviate GRAM usage
        scores = []
        chunk_size = self.args.data.eval_chunk_size
        for idx in range(math.ceil(self.args.data.num_entity / chunk_size)):
            start_pos = idx * chunk_size
            end_pos = (idx + 1) * chunk_size

            chunk_entity_text_embeds = self.entity_text_embeds[start_pos:end_pos].to(mention_text_embeds.device)
            chunk_entity_image_embeds = self.entity_image_embeds[start_pos:end_pos].to(mention_text_embeds.device)
            chunk_entity_text_seq_tokens = self.entity_text_seq_tokens[start_pos:end_pos].to(mention_text_embeds.device)
            chunk_entity_image_patch_tokens = self.entity_image_patch_tokens[start_pos:end_pos].to(
                mention_text_embeds.device)

            chunk_score, _ = self.matcher(chunk_entity_text_embeds, chunk_entity_text_seq_tokens,
                                          mention_text_embeds, mention_text_seq_tokens,
                                          chunk_entity_image_embeds, chunk_entity_image_patch_tokens,
                                          mention_image_embeds, mention_image_patch_tokens)
            scores.append(chunk_score)

        scores = torch.concat(scores, dim=-1)
        rank = torch.argsort(torch.argsort(scores, dim=-1, descending=True), dim=-1, descending=False) + 1
        tgt_rank = rank[torch.arange(batch_size), answer].detach().cpu()
        return dict(rank=tgt_rank, all_rank=rank.detach().cpu().numpy(), scores=scores.detach().cpu().numpy())

    def on_test_start(self):
        # Update entity embedding before test starts
        # Note that we use entity_dataloader defined in our datamodule (please see codes/utils/dataset)
        entity_dataloader = self.trainer.datamodule.entity_dataloader()
        outputs_text_embed = []
        outputs_image_embed = []
        outputs_text_seq_tokens = []
        outputs_image_patch_tokens = []

        with torch.no_grad():
            for batch in tqdm(entity_dataloader, desc='UpdateEmbed', total=len(entity_dataloader)):
                batch = pl.utilities.move_data_to_device(batch, self.device)
                entity_text_embeds, entity_image_embeds, entity_text_seq_tokens, entity_image_patch_tokens = \
                    self.encoder(**batch)
                outputs_text_embed.append(entity_text_embeds.cpu())
                outputs_image_embed.append(entity_image_embeds.cpu())
                outputs_text_seq_tokens.append(entity_text_seq_tokens.cpu())
                outputs_image_patch_tokens.append(entity_image_patch_tokens.cpu())

        self.entity_text_embeds = torch.concat(outputs_text_embed, dim=0)
        self.entity_image_embeds = torch.concat(outputs_image_embed, dim=0)
        self.entity_text_seq_tokens = torch.concat(outputs_text_seq_tokens, dim=0)
        self.entity_image_patch_tokens = torch.concat(outputs_image_patch_tokens, dim=0)

    def test_epoch_end(self, outputs):
        self.entity_text_embeds = None
        self.entity_image_embeds = None
        self.entity_text_seq_tokens = None
        self.entity_image_patch_tokens = None

        ranks = np.concatenate([_['rank'] for _ in outputs])
        hits20 = (ranks <= 20).mean()
        hits10 = (ranks <= 10).mean()
        hits5 = (ranks <= 5).mean()
        hits3 = (ranks <= 3).mean()
        hits1 = (ranks <= 1).mean()

        self.log("Test/hits20", hits20)
        self.log("Test/hits10", hits10)
        self.log("Test/hits5", hits5)
        self.log("Test/hits3", hits3)
        self.log("Test/hits1", hits1)
        self.log("Test/mr", ranks.mean())
        self.log("Test/mrr", (1. / ranks).mean())

    def configure_optimizers(self):
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_grouped_params = [
            {'params': [p for n, p in self.named_parameters() if not any(nd in n for nd in no_decay)],
             'weight_decay': 0.0001},
            {'params': [p for n, p in self.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]
        optimizer = torch.optim.AdamW(optimizer_grouped_params, lr=self.args.lr, betas=(0.9, 0.999), eps=1e-4)
        return [optimizer]
