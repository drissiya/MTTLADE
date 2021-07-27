import os
from sys import path
path.append(os.getcwd())
from ade_extraction.common import get_label_mappers, get_predicted_sequence_2
from ade_extraction.tac.extract import extract_att_rel_tac
from ade_extraction.tac.utils import write_guess_xml_files
from ade_extraction.n2c2.extract import extract_att_relation_n2c2
from ade_extraction.n2c2.utils import write_brat_files

import codecs
import pickle as pkl
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description="ADE-Att-RE task")
    parser.add_argument('--dataset', type=str, default='tac',
                        help='tac/n2c2')
    parser.add_argument('--predicted_json_path', type=str, default='checkpoint/tacrelation_pred_scores_0.json')
    parser.add_argument('--gold_json_path', type=str, default='data/canonical_data/bert_uncased_lower/tacrelation_test.json')
    parser.add_argument('--gold_xml_dir', type=str, default='data/ADR/TAC/gold_xml')
    parser.add_argument('--guess_xml_dir', type=str, default='data/ADR/TAC/guess_xml')
    parser.add_argument('--guess_n2c2_dir', type=str, default='data/ADR/N2C2/test_data_Tasks1&3/')
    args = parser.parse_args()
    label_mappers = get_label_mappers()
    if args.dataset=='tac':
        with open('data/ADR/TAC/dict_ade.pkl', 'rb') as f: 
            dict_ade = pkl.load(f)

        with open('data/ADR/TAC/list_id_mentions.pkl', 'rb') as f: 
            list_id_mentions = pkl.load(f)
            
        with open('data/ADR/TAC/ade_set.pkl', 'rb') as f: 
            ade_set = pkl.load(f)
            
        TAC_guess = get_predicted_sequence_2(label_mappers=label_mappers[1],
                                              dataset=args.dataset,
                                              predicted_json_path=args.predicted_json_path, 
                                              gold_json_path=args.gold_json_path)
        dict_modifiers, dict_relations = extract_att_rel_tac(TAC_guess, list_id_mentions, ade_set)
        #print (dict_relations)
        os.makedirs(args.guess_xml_dir, exist_ok=True)
        write_guess_xml_files(args.gold_xml_dir,
                              args.guess_xml_dir,
                              dict_ade,
                              dict_modifiers,
                              dict_relations)

    if args.dataset=='n2c2':
        with open('data/ADR/N2C2/dict_drug.pkl', 'rb') as f: 
            dict_drug = pkl.load(f)

        with open('data/ADR/N2C2/list_id_mentions.pkl', 'rb') as f: 
            list_id_mentions = pkl.load(f)
            
        with open('data/ADR/N2C2/ade_set.pkl', 'rb') as f: 
            ade_set = pkl.load(f)
            
        N2C2_guess = get_predicted_sequence_2(label_mappers=label_mappers[3],
                                              dataset=args.dataset,
                                              predicted_json_path=args.predicted_json_path, 
                                              gold_json_path=args.gold_json_path)
        dict_modifiers, dict_relations = extract_att_relation_n2c2(N2C2_guess, ade_set, list_id_mentions)
        #print (dict_relations)

        write_brat_files(args.guess_n2c2_dir,
                         dict_drug,
                         dict_modifiers,
                         dict_relations)

