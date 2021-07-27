import os
from sys import path
path.append(os.getcwd())
from data_utils.task_def import DataFormat

def load_adr_ner(tac_data):
    rows = []
    cnt = 0
    for sentence, label, start, section, lenn, drug, sentence_input, start_sentence, len_sentence in zip(tac_data.t_toks_mention, tac_data.t_segment_mention, tac_data.t_start_mention, tac_data.t_section_mention, tac_data.t_len_mention, tac_data.t_drug_mention, tac_data.t_sentence_input_mention, tac_data.t_start_sentence_mention, tac_data.t_len_sentence_mention):
        sample = {'uid': cnt, 'premise': sentence, 'label': label, 'start': start, 'section': section, 'lenn': lenn, 'drug': drug, 'sentence_input': [sentence_input], 'start_sentence': [start_sentence], 'len_sentence': [len_sentence], 'token': sentence, 'ade': sentence, 'modifier': sentence}
        rows.append(sample)
        cnt += 1
    return rows
	
def load_adr_relation(tac_data):
    rows = []
    cnt = 0
    for sentence, label, ade, token, start, section, lenn, drug, modifier in zip(tac_data.t_sentence_relation, tac_data.t_segment_relation, tac_data.t_ade, tac_data.t_toks_relation, tac_data.t_start_relation, tac_data.t_section_relation, tac_data.t_len_relation, tac_data.t_drug_relation, tac_data.t_modifiers):
        sample = {'uid': cnt, 'premise': sentence, 'label': label, 'start': start, 'section': section, 'lenn': lenn, 'drug': drug, 'sentence_input': token, 'start_sentence': token, 'len_sentence': token, 'token': token, 'ade': list(ade), 'modifier': list(modifier)}
        rows.append(sample)
        cnt += 1 
    return rows
	
