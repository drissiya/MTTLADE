import os
from sys import path
path.append(os.getcwd())
from ade_extraction.common import get_label_mappers, get_predicted_sequence_1
from ade_extraction.tac.extract import extract_source_mention_tac
from ade_extraction.n2c2.extract import extract_source_mention_n2c2

import codecs
import pickle as pkl
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description="ADE-SE task")
    parser.add_argument('--dataset', type=str, default='tac',
                        help='tac/n2c2')
    parser.add_argument('--predicted_rel_json_path', type=str, default='checkpoint/tacsource_test_scores_8.json')
    parser.add_argument('--gold_rel_json_path', type=str, default='data/canonical_data/bert_uncased_lower/tacsource_test.json')
    parser.add_argument('--data_dir', type=str, default='data/ADR')

    args = parser.parse_args()
    label_mappers = get_label_mappers()
    if args.dataset=='tac':
        TAC_guess = get_predicted_sequence_1(label_mappers=label_mappers[0],
                                              dataset=args.dataset,
                                              predicted_rel_json_path=args.predicted_rel_json_path, 
                                              gold_rel_json_path=args.gold_rel_json_path)
        TAC_guess, dict_ade, list_id_mentions, ade_set = extract_source_mention_tac(TAC_guess)
        print (len(TAC_guess.t_drug_relation))
        print (TAC_guess.t_toks_relation[1])
        print (TAC_guess.t_sentence_relation[1])
        print (TAC_guess.t_segment_relation[1])
        print (TAC_guess.t_section_relation[1])
        print (TAC_guess.t_start_relation[1])
        print (TAC_guess.t_len_relation[1])
        print (TAC_guess.t_ade[1])
        print (TAC_guess.t_modifiers[1])  

        with codecs.open('data/ADR/TAC/tac_guess.pkl', 'wb') as w:
            pkl.dump(TAC_guess, w)

        with codecs.open('data/ADR/TAC/dict_ade.pkl', 'wb') as w:
            pkl.dump(dict_ade, w)

        with codecs.open('data/ADR/TAC/list_id_mentions.pkl', 'wb') as w:
            pkl.dump(list_id_mentions, w)

        with codecs.open('data/ADR/TAC/ade_set.pkl', 'wb') as w:
            pkl.dump(ade_set, w)
			
    if args.dataset=='n2c2':
        N2C2_guess = get_predicted_sequence_1(label_mappers=label_mappers[2],
                                              dataset=args.dataset,
                                              predicted_rel_json_path=args.predicted_rel_json_path, 
                                              gold_rel_json_path=args.gold_rel_json_path)
        N2C2_guess, dict_drug, list_id_mentions, ade_set = extract_source_mention_n2c2(N2C2_guess)
        print (N2C2_guess.t_sentence_relation[1])
        print (N2C2_guess.t_toks_relation[1])
        print (N2C2_guess.t_segment_relation[1])
        print (N2C2_guess.t_start_relation[1])
        print (N2C2_guess.t_section_relation[1])
        print (N2C2_guess.t_len_relation[1])
        print (N2C2_guess.t_ade[1])
        print (N2C2_guess.t_modifiers[1])
        print (N2C2_guess.t_drug_relation[1])

        with codecs.open('data/ADR/N2C2/N2C2_guess.pkl', 'wb') as w:
            pkl.dump(N2C2_guess, w)

        with codecs.open('data/ADR/N2C2/dict_drug.pkl', 'wb') as w:
            pkl.dump(dict_drug, w)

        with codecs.open('data/ADR/N2C2/list_id_mentions.pkl', 'wb') as w:
            pkl.dump(list_id_mentions, w)

        with codecs.open('data/ADR/N2C2/ade_set.pkl', 'wb') as w:
            pkl.dump(ade_set, w)