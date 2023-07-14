import math
import torch
import torch.nn as nn
from transformers import CLIPModel


class MIMICEncoder(nn.Module):
    def __init__(self, args):
        super(MIMICEncoder, self).__init__()
        self.args = args
        self.clip = CLIPModel.from_pretrained(self.args.pretrained_model)

        self.image_cls_fc = nn.Linear(self.args.model.input_hidden_dim, self.args.model.dv)
        self.image_tokens_fc = nn.Linear(self.args.model.input_image_hidden_dim, self.args.model.dv)

    def forward(self,
                input_ids=None,
                attention_mask=None,
                token_type_ids=None,
                pixel_values=None):
        clip_output = self.clip(input_ids=input_ids,
                                attention_mask=attention_mask,
                                pixel_values=pixel_values)

        text_embeds = clip_output.text_embeds
        image_embeds = clip_output.image_embeds

        text_seq_tokens = clip_output.text_model_output[0]
        image_patch_tokens = clip_output.vision_model_output[0]

        image_embeds = self.image_cls_fc(image_embeds)
        image_patch_tokens = self.image_tokens_fc(image_patch_tokens)
        return text_embeds, image_embeds, text_seq_tokens, image_patch_tokens


class TextBasedGlobalLocalUnit(nn.Module):
    def __init__(self, args):
        super(TextBasedGlobalLocalUnit, self).__init__()
        self.args = args
        self.fc_query = nn.Linear(self.args.model.input_hidden_dim, self.args.model.TGLU_hidden_dim)
        self.fc_key = nn.Linear(self.args.model.input_hidden_dim, self.args.model.TGLU_hidden_dim)
        self.fc_value = nn.Linear(self.args.model.input_hidden_dim, self.args.model.TGLU_hidden_dim)
        self.fc_cls = nn.Linear(self.args.model.input_hidden_dim, self.args.model.TGLU_hidden_dim)
        self.layer_norm = nn.LayerNorm(self.args.model.TGLU_hidden_dim)

    def forward(self,
                entity_text_cls,
                entity_text_tokens,
                mention_text_cls,
                mention_text_tokens):
        """

        :param entity_text_cls:     [num_entity, dim]
        :param entity_text_tokens:  [num_entity, max_seq_len, dim]
        :param mention_text_cls:    [batch_size, dim]
        :param mention_text_tokens: [batch_size, max_sqe_len, dim]
        :return:
        """

        entity_cls_fc = self.fc_cls(entity_text_cls)  # [num_entity, dim]
        entity_cls_fc = entity_cls_fc.unsqueeze(dim=1)  # [num_entity, 1, dim]

        query = self.fc_query(entity_text_tokens)  # [num_entity, max_seq_len, dim]
        key = self.fc_key(mention_text_tokens)  # [batch_size, max_sqe_len, dim]
        value = self.fc_value(mention_text_tokens)  # [batch_size, max_sqe_len, dim]

        query = query.unsqueeze(dim=1)  # [num_entity, 1, max_seq_len, dim]
        key = key.unsqueeze(dim=0)  # [1, batch_size, max_sqe_len, dim]
        value = value.unsqueeze(dim=0)  # [1, batch_size, max_sqe_len, dim]

        attention_scores = torch.matmul(query,
                                        key.transpose(-1, -2))  # [num_entity, batch_size, max_seq_len, max_seq_len]

        attention_scores = attention_scores / math.sqrt(self.args.model.TGLU_hidden_dim)
        attention_probs = nn.Softmax(dim=-1)(attention_scores)  # [num_entity, batch_size, max_seq_len, max_seq_len]

        context = torch.matmul(attention_probs, value)  # [num_entity, batch_size, max_seq_len, dim]
        context = torch.mean(context, dim=-2)  # [num_entity, batch_size, dim]
        context = self.layer_norm(context)

        g2l_matching_score = torch.sum(entity_cls_fc * context, dim=-1)  # [num_entity, batch_size]
        g2l_matching_score = g2l_matching_score.transpose(0, 1)  # [batch_size, num_entity]
        g2g_matching_score = torch.matmul(mention_text_cls, entity_text_cls.transpose(-1, -2))

        matching_score = (g2l_matching_score + g2g_matching_score) / 2
        return matching_score


class DUAL(nn.Module):
    def __init__(self, args):
        super(DUAL, self).__init__()
        self.args = args
        self.cls_fc = nn.Linear(self.args.model.dv, self.args.model.IDLU_hidden_dim)
        self.tokens_fc = nn.Linear(self.args.model.dv, self.args.model.IDLU_hidden_dim)
        self.fc = nn.Linear(self.args.model.IDLU_hidden_dim, self.args.model.IDLU_hidden_dim)
        self.gate_fc = nn.Linear(self.args.model.IDLU_hidden_dim, 1)
        self.activation = nn.Tanh()
        self.add_layer_norm = nn.LayerNorm(self.args.model.IDLU_hidden_dim)
        self.layer_norm = nn.LayerNorm(self.args.model.IDLU_hidden_dim)

    def forward(self,
                query_cls,
                key_cls,
                value_tokens):
        """

        :param query_cls:       [a, dim]
        :param key_cls:         [b, dim]
        :param value_tokens:    [b, num_patch, dim]
        :return:
        """
        query_cls = self.cls_fc(query_cls)
        key_cls = self.cls_fc(key_cls)
        value_tokens = self.tokens_fc(value_tokens)

        value_pooled = torch.mean(value_tokens, dim=-2)  # [b, dim]
        value = value_pooled.unsqueeze(dim=0)  # [1, b, dim]
        query = query_cls.unsqueeze(dim=1)  # [a, 1, dim]
        context = self.add_layer_norm(value + query)
        context = self.fc(context)  # [a, b, dim]

        gate_value = self.activation(self.gate_fc(context))  # [a, b, 1]
        aggregated_value = (context * gate_value) + key_cls.unsqueeze(dim=0)  # [a, b, dim]
        aggregated_value = self.layer_norm(aggregated_value)  # [a, b, dim]

        query_cls = self.layer_norm(query)  # [a, 1, dim]
        score = torch.sum(aggregated_value * query_cls, dim=-1)
        return score


class VisionBasedDualUnit(nn.Module):
    def __init__(self, args):
        super(VisionBasedDualUnit, self).__init__()
        self.args = args

        self.dual_ent2men = DUAL(self.args)     # dual function from entity to mention
        self.dual_men2ent = DUAL(self.args)     # dual function from mention to entity

    def forward(self,
                entity_image_cls, entity_image_tokens,
                mention_image_cls, mention_image_tokens):
        """
        :param entity_image_cls:        [num_entity, dim]
        :param entity_image_tokens:     [num_entity, num_patch, dim]
        :param mention_image_cls:       [batch_size, dim]
        :param mention_image_tokens:    [batch_size, num_patch, dim]
        :return:
        """

        entity_to_mention_score = self.dual_ent2men(entity_image_cls, mention_image_cls, mention_image_tokens)
        mention_to_entity_score = self.dual_men2ent(mention_image_cls, entity_image_cls, entity_image_tokens)

        dual_score = (entity_to_mention_score.transpose(0, 1) + mention_to_entity_score) / 2  # [batch_size, num_entity]
        return dual_score


class CrossModalFusionUnit(nn.Module):
    def __init__(self, args):
        super(CrossModalFusionUnit, self).__init__()
        self.args = args
        self.text_fc = nn.Linear(self.args.model.input_hidden_dim, self.args.model.CMFU_hidden_dim)
        self.image_fc = nn.Linear(self.args.model.dv, self.args.model.CMFU_hidden_dim)
        self.gate_fc = nn.Linear(self.args.model.CMFU_hidden_dim, 1)
        self.gate_act = nn.Tanh()
        self.gate_layer_norm = nn.LayerNorm(self.args.model.CMFU_hidden_dim)
        self.context_layer_norm = nn.LayerNorm(self.args.model.CMFU_hidden_dim)

    def forward(self, entity_text_cls, entity_image_tokens,
                mention_text_cls, mention_image_tokens):
        """
        :param entity_text_cls:         [num_entity, dim]
        :param entity_image_tokens:     [num_entity, num_patch, dim]
        :param mention_text_cls:        [batch_size, dim]
        :param mention_image_tokens:    [batch_size, num_patch, dim]
        :return:
        """
        entity_text_cls = self.text_fc(entity_text_cls)  # [num_entity, dim]
        entity_text_cls_ori = entity_text_cls
        mention_text_cls = self.text_fc(mention_text_cls)  # [batch_size, dim]
        mention_text_cls_ori = mention_text_cls

        entity_image_tokens = self.image_fc(entity_image_tokens)  # [num_entity, num_patch, dim]
        mention_image_tokens = self.image_fc(mention_image_tokens)  # [batch_size, num_patch, dim]

        entity_text_cls = entity_text_cls.unsqueeze(dim=1)  # [num_entity, 1, dim]
        entity_cross_modal_score = torch.matmul(entity_text_cls, entity_image_tokens.transpose(-1, -2))
        entity_cross_modal_probs = nn.Softmax(dim=-1)(entity_cross_modal_score)  # [num_entity, 1, num_patch]
        entity_context = torch.matmul(entity_cross_modal_probs, entity_image_tokens).squeeze()  # [num_entity, 1, dim]
        entity_gate_score = self.gate_act(self.gate_fc(entity_text_cls_ori))
        entity_context = self.gate_layer_norm((entity_text_cls_ori * entity_gate_score) + entity_context)

        mention_text_cls = mention_text_cls.unsqueeze(dim=1)  # [batch_size, 1, dim]
        mention_cross_modal_score = torch.matmul(mention_text_cls, mention_image_tokens.transpose(-1, -2))
        mention_cross_modal_probs = nn.Softmax(dim=-1)(mention_cross_modal_score)
        mention_context = torch.matmul(mention_cross_modal_probs, mention_image_tokens).squeeze()
        mention_gate_score = self.gate_act(self.gate_fc(mention_text_cls_ori))
        mention_context = self.gate_layer_norm((mention_text_cls_ori * mention_gate_score) + mention_context)

        score = torch.matmul(mention_context, entity_context.transpose(-1, -2))
        return score


class MIMICMatcher(nn.Module):
    def __init__(self, args):
        super(MIMICMatcher, self).__init__()
        self.args = args
        self.tglu = TextBasedGlobalLocalUnit(self.args)  # TGLU
        self.vdlu = VisionBasedDualUnit(self.args)  # VDLU
        self.cmfu = CrossModalFusionUnit(self.args)  # CMFU

        self.text_cls_layernorm = nn.LayerNorm(self.args.model.dt)
        self.text_tokens_layernorm = nn.LayerNorm(self.args.model.dt)
        self.image_cls_layernorm = nn.LayerNorm(self.args.model.dv)
        self.image_tokens_layernorm = nn.LayerNorm(self.args.model.dv)

    def forward(self,
                entity_text_cls, entity_text_tokens,
                mention_text_cls, mention_text_tokens,
                entity_image_cls, entity_image_tokens,
                mention_image_cls, mention_image_tokens):
        """

        :param entity_text_cls:     [num_entity, dim]
        :param entity_text_tokens:  [num_entity, max_seq_len, dim]
        :param mention_text_cls:    [batch_size, dim]
        :param mention_text_tokens: [batch_size, max_sqe_len, dim]
        :param entity_image_cls:    [num_entity, dim]
        :param mention_image_cls:   [batch_size, dim]
        :param entity_image_tokens: [num_entity, num_patch, dim]
        :param mention_image_tokens:[num_entity, num_patch, dim]
        :return:
        """
        entity_text_cls = self.text_cls_layernorm(entity_text_cls)
        mention_text_cls = self.text_cls_layernorm(mention_text_cls)

        entity_text_tokens = self.text_tokens_layernorm(entity_text_tokens)
        mention_text_tokens = self.text_tokens_layernorm(mention_text_tokens)

        entity_image_cls = self.image_cls_layernorm(entity_image_cls)
        mention_image_cls = self.image_cls_layernorm(mention_image_cls)

        entity_image_tokens = self.image_tokens_layernorm(entity_image_tokens)
        mention_image_tokens = self.image_tokens_layernorm(mention_image_tokens)

        text_matching_score = self.tglu(entity_text_cls, entity_text_tokens,
                                        mention_text_cls, mention_text_tokens)
        image_matching_score = self.vdlu(entity_image_cls, entity_image_tokens,
                                         mention_image_cls, mention_image_tokens)
        image_text_matching_score = self.cmfu(entity_text_cls, entity_image_tokens,
                                              mention_text_cls, mention_image_tokens)

        score = (text_matching_score + image_matching_score + image_text_matching_score) / 3
        return score, (text_matching_score, image_matching_score, image_text_matching_score)
