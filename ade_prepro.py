import os
import argparse
import pickle as pkl
from sys import path
path.append(os.getcwd())
from data_utils.task_def import DataFormat
from data_utils.tac.tac_corpus import TAC, split_data_sequence_tac
from data_utils.n2c2.n2c2_corpus import N2C2, split_data_sequence_n2c2
from data_utils.log_wrapper import create_logger
from experiments.adr_utils import *
from experiments.common_utils import dump_rows
logger = create_logger(__name__, to_disk=True, log_file='bert_ner_data_proc_512_cased.log')

def parse_args():
    parser = argparse.ArgumentParser(description='Preprocessing ADR datasets.')
    parser.add_argument('--data_dir', type=str, default="data/ADR")
    parser.add_argument('--seed', type=int, default=13)
    parser.add_argument('--output_dir', type=str, default="data/canonical_data")
    args = parser.parse_args()
    return args

def main(args):
    data_dir = args.data_dir
    data_dir = os.path.abspath(data_dir)
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
        
    print ("Load TAC training set") 
    TAC_train_temp = TAC(os.path.join(data_dir, "TAC", "TR"), os.path.join(data_dir, "TAC", "train_xml")) 
    TAC_train_temp.load_corpus()    
    TAC_train, TAC_dev = split_data_sequence_tac(TAC_train_temp)
    
    print ("Load TAC test set")
    TAC_test = TAC(os.path.join(data_dir, "TAC", "TE"), os.path.join(data_dir, "TAC", "gold_xml")) 
    TAC_test.load_corpus()
	
    print ("Load n2c2 training set")
    n2c2_train_temp = N2C2(label_dir=data_dir+"/N2C2/training_20180910/")
    n2c2_train_temp.load_corpus()    
    n2c2_train, n2c2_dev = split_data_sequence_n2c2(n2c2_train_temp)
    
    print ("Load n2c2 test set")
    n2c2_test = N2C2(label_dir=data_dir+"/N2C2/test/")
    n2c2_test.load_corpus() 

    
    train_tac_ner = load_adr_ner(TAC_train)
    print (train_tac_ner[0])
    dev_tac_ner = load_adr_ner(TAC_dev)
    print (dev_tac_ner[0])
    test_tac_ner = load_adr_ner(TAC_test)
    print (test_tac_ner[0])

    logger.info('Loaded {} TAC NER rel train samples'.format(len(train_tac_ner)))
    logger.info('Loaded {} TAC NER rel dev samples'.format(len(dev_tac_ner)))
    logger.info('Loaded {} TAC NER rel test samples'.format(len(test_tac_ner)))
        

    train_tac_relation = load_adr_relation(TAC_train)
    print (train_tac_relation[0])
    dev_tac_relation = load_adr_relation(TAC_dev)
    print (dev_tac_relation[0])
    test_tac_relation = load_adr_relation(TAC_test)
    print (test_tac_relation[0])

    logger.info('Loaded {} TAC Relation train samples'.format(len(train_tac_relation)))
    logger.info('Loaded {} TAC Relation dev samples'.format(len(dev_tac_relation)))
    logger.info('Loaded {} TAC Relation test samples'.format(len(test_tac_relation)))
	
    train_n2c2_ner = load_adr_ner(n2c2_train)
    print (train_n2c2_ner[0])
    dev_n2c2_ner = load_adr_ner(n2c2_dev)
    print (dev_n2c2_ner[0])
    test_n2c2_ner = load_adr_ner(n2c2_test)
    print (test_n2c2_ner[0])

    logger.info('Loaded {} n2c2 NER train samples'.format(len(train_n2c2_ner)))
    logger.info('Loaded {} n2c2 NER dev samples'.format(len(dev_n2c2_ner)))
    logger.info('Loaded {} n2c2 NER test samples'.format(len(test_n2c2_ner)))
	
    train_n2c2_relation = load_adr_relation(n2c2_train)
    print (train_n2c2_relation[0])
    dev_n2c2_relation = load_adr_relation(n2c2_dev)
    print (dev_n2c2_relation[0])
    test_n2c2_relation = load_adr_relation(n2c2_test)
    print (test_n2c2_relation[0])

    logger.info('Loaded {} n2c2 Relation train samples'.format(len(train_n2c2_relation)))
    logger.info('Loaded {} n2c2 Relation dev samples'.format(len(dev_n2c2_relation)))
    logger.info('Loaded {} n2c2 Relation test samples'.format(len(test_n2c2_relation)))
	


    bert_root = args.output_dir
    if not os.path.isdir(bert_root):
        os.mkdir(bert_root)
	


    train_fout = os.path.join(bert_root, 'tacsource_train.tsv')
    dev_fout = os.path.join(bert_root, 'tacsource_dev.tsv')
    test_fout = os.path.join(bert_root, 'tacsource_test.tsv')

    dump_rows(train_tac_ner, train_fout, DataFormat.Seqence)
    dump_rows(dev_tac_ner, dev_fout, DataFormat.Seqence)
    dump_rows(test_tac_ner, test_fout, DataFormat.Seqence)
    logger.info('done with TAC source')
	

    train_fout = os.path.join(bert_root, 'tacrelation_train.tsv')
    dev_fout = os.path.join(bert_root, 'tacrelation_dev.tsv')
    test_fout = os.path.join(bert_root, 'tacrelation_test.tsv')
    
    dump_rows(train_tac_relation, train_fout, DataFormat.Seqence)
    dump_rows(dev_tac_relation, dev_fout, DataFormat.Seqence)
    dump_rows(test_tac_relation, test_fout, DataFormat.Seqence)
    logger.info('done with TAC Relation')
	
    train_fout = os.path.join(bert_root, 'n2c2source_train.tsv')
    dev_fout = os.path.join(bert_root, 'n2c2source_dev.tsv')
    test_fout = os.path.join(bert_root, 'n2c2source_test.tsv')

    dump_rows(train_n2c2_ner, train_fout, DataFormat.Seqence)
    dump_rows(dev_n2c2_ner, dev_fout, DataFormat.Seqence)
    dump_rows(test_n2c2_ner, test_fout, DataFormat.Seqence)
    logger.info('done with n2c2 source')
	

    train_fout = os.path.join(bert_root, 'n2c2relation_train.tsv')
    dev_fout = os.path.join(bert_root, 'n2c2relation_dev.tsv')
    test_fout = os.path.join(bert_root, 'n2c2relation_test.tsv')
    
    dump_rows(train_n2c2_relation, train_fout, DataFormat.Seqence)
    dump_rows(dev_n2c2_relation, dev_fout, DataFormat.Seqence)
    dump_rows(test_n2c2_relation, test_fout, DataFormat.Seqence)
    logger.info('done with n2c2 Relation')


	




	
if __name__ == '__main__':
    args = parse_args()
    main(args)