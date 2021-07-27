import os
import argparse
import pickle as pkl
from sys import path
path.append(os.getcwd())
from data_utils.task_def import DataFormat
from data_utils.log_wrapper import create_logger
from experiments.adr_utils import load_adr_ner, load_adr_relation
from experiments.common_utils import dump_rows
logger = create_logger(__name__, to_disk=True, log_file='bert_ner_data_proc_512_cased.log')

def parse_args():
    parser = argparse.ArgumentParser(description='Preprocessing ADR dataset.')
    parser.add_argument('--data_dir', type=str, default="data/ADR")
    parser.add_argument('--dataset', type=str, default="tac", help='tac/n2c2')
    parser.add_argument('--seed', type=int, default=13)
    parser.add_argument('--output_dir', type=str, default="data/canonical_data")
    args = parser.parse_args()
    return args

def main(args):
    data_dir = args.data_dir
    data_dir = os.path.abspath(data_dir)
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    
    if args.dataset=='tac':
        #Load TAC test set
        with open(data_dir+'/TAC/tac_guess.pkl', 'rb') as f: 
            TAC_test = pkl.load(f)

        test_relation = load_adr_relation(TAC_test)

        logger.info('Loaded {} TAC Relation test samples'.format(len(test_relation)))


        bert_root = args.output_dir
        if not os.path.isdir(bert_root):
            os.mkdir(bert_root)

        test_fout = os.path.join(bert_root, 'tacrelation_test.tsv')

        dump_rows(test_relation, test_fout, DataFormat.Seqence)
        logger.info('done with TAC Relation')    

    if args.dataset=='n2c2':
        #Load n2c2 test set
        with open(data_dir+'/N2C2/N2C2_guess.pkl', 'rb') as f: 
            N2C2_guess = pkl.load(f)

        test_relation = load_adr_relation(N2C2_guess)

        logger.info('Loaded {} N2C2 Relation test samples'.format(len(test_relation)))


        bert_root = args.output_dir
        if not os.path.isdir(bert_root):
            os.mkdir(bert_root)

        test_fout = os.path.join(bert_root, 'n2c2relation_test.tsv')

        dump_rows(test_relation, test_fout, DataFormat.Seqence)
        logger.info('done with N2C2 Relation') 
if __name__ == '__main__':
    args = parse_args()
    main(args)