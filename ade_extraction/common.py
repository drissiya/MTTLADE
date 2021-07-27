import yaml
import json

from data_utils.task_def import TaskType, DataFormat
from data_utils.tac.tac_corpus import TAC
from data_utils.n2c2.n2c2_corpus import N2C2
from experiments.exp_def import TaskDefs

def get_label_mappers(path_yml="ade_task_def.yml"):
    task_defs = TaskDefs(path_yml)
    task_def_dic = yaml.safe_load(open(path_yml))
    label_mappers = []
    for task, task_def in task_def_dic.items():
        data_format = DataFormat[task_def["data_format"]]
        task_type = TaskType[task_def["task_type"]]
        label_mapper = task_defs.global_map.get(task, None)
        label_mappers.append(label_mapper)
    return label_mappers 
	
def trim_sequence(prediction, true_set, label_mappers):
    predict_lines = []
    for pred, true in zip(prediction, true_set):
        p_label = []
        for p, t in zip(pred, true):
            l= label_mappers.ind2tok[p]
            tr= label_mappers.ind2tok[t]
            if tr == 'X': continue
            if l == 'CLS': continue
            if l == 'SEP': continue
            if l == 'X': l = 'O'
            p_label.append(l)
        predict_lines.append(p_label)
    return predict_lines
	
def get_predicted_sequence_1(label_mappers,
                             dataset,
                             predicted_rel_json_path, 
                             gold_rel_json_path):
    if dataset=='tac':
        data_test = TAC() 
    if dataset=='n2c2':
        data_test = N2C2()
        
    with open(predicted_rel_json_path) as json_file:
        data = json.load(json_file)
        prediction_rel = data["predictions"]


    data = [json.loads(line) for line in open(gold_rel_json_path, 'r')]
    for p in data:
        data_test.t_segment_mention.append(p["label"])
        data_test.t_toks_mention.append(p["tokens"])
        data_test.t_start_mention.append(p["start"])
        data_test.t_section_mention.append(p["section"])
        data_test.t_len_mention.append(p["lenn"])
        data_test.t_drug_mention.append(p["drug"])
        data_test.t_sentence_input_mention.append(p["sentence_input"][0])
        data_test.t_start_sentence_mention.append(p["start_sentence"][0])
        data_test.t_len_sentence_mention.append(p["len_sentence"][0])

    predicted_sequence_rel = trim_sequence(prediction_rel, data_test.t_segment_mention, label_mappers)
    data_test.t_segment_mention = predicted_sequence_rel

    return data_test
	
def get_predicted_sequence_2(label_mappers,
                             dataset,
                             predicted_json_path='checkpoint/tacrelation_pred_scores_0.json', 
                             gold_json_path='data/canonical_data/bert_uncased_lower/tacrelation_test.json'):
    if dataset=='tac':
        data_test = TAC() 
    if dataset=='n2c2':
        data_test = N2C2() 
    with open(predicted_json_path) as json_file:
        data = json.load(json_file)
        prediction = data["predictions"]

    data = [json.loads(line) for line in open(gold_json_path, 'r')]
    for p in data:
        data_test.t_sentence_relation.append(p["tokens"])
        data_test.t_toks_relation.append(p["tokens"])
        data_test.t_segment_relation.append(p["label"])
        data_test.t_start_relation.append(p["start"])
        data_test.t_section_relation.append(p["section"])
        data_test.t_len_relation.append(p["lenn"])
        data_test.t_ade.append(p["ade"])
        data_test.t_modifiers.append(p["modifier"])
        data_test.t_drug_relation.append(p["drug"])
    predicted_sequence = trim_sequence(prediction, data_test.t_segment_relation, label_mappers)

    data_test.t_segment_relation = predicted_sequence

    return data_test