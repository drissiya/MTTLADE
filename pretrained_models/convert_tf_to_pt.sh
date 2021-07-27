#!/usr/bin/env bash



## BERT 
cd  "pretrained_models"
mkdir "bert"
wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip -O "uncased_L-12_H-768_A-12.zip"
unzip uncased_L-12_H-768_A-12.zip -d "bert"
rm "uncased_L-12_H-768_A-12.zip"
mv "bert/uncased_L-12_H-768_A-12/vocab.txt" "bert/vocab.txt"
mv "bert/uncased_L-12_H-768_A-12/bert_model.ckpt.meta" "bert/bert_model.ckpt.meta"
mv "bert/uncased_L-12_H-768_A-12/bert_model.ckpt.data-00000-of-00001" "bert/bert_model.ckpt.data-00000-of-00001"
mv "bert/uncased_L-12_H-768_A-12/bert_model.ckpt.index" "bert/bert_model.ckpt.index"
mv "bert/uncased_L-12_H-768_A-12/bert_config.json" "bert/bert_config.json"
rm -r "bert/uncased_L-12_H-768_A-12/"

python convert_tf_to_pt.py \
    --tf-path-model "bert/bert_model.ckpt" \
    --config-file "bert/bert_config.json" \
    --model-type "bert" \
    --pytorch-file "bert_base_uncased.pt" \

rm -r "bert/"

## SCIBERT
cd  "pretrained_models"
mkdir "scibert_vocab"
wget https://s3-us-west-2.amazonaws.com/ai2-s2-research/scibert/tensorflow_models/scibert_scivocab_uncased.tar.gz -O "scibert_scivocab_uncased.tar.gz"
tar xvf scibert_scivocab_uncased.tar.gz
rm "scibert_scivocab_uncased.tar.gz"
mv "scibert_scivocab_uncased/vocab.txt" "scibert_vocab/vocab.txt"
mv "scibert_scivocab_uncased/bert_model.ckpt.meta" "scibert_vocab/bert_model.ckpt.meta"
mv "scibert_scivocab_uncased/bert_model.ckpt.data-00000-of-00001" "scibert_vocab/bert_model.ckpt.data-00000-of-00001"
mv "scibert_scivocab_uncased/bert_model.ckpt.index" "scibert_vocab/bert_model.ckpt.index"
mv "scibert_scivocab_uncased/bert_config.json" "scibert_vocab/bert_config.json"
rm -r "scibert_scivocab_uncased/"

python convert_tf_to_pt.py \
    --tf-path-model "scibert_vocab/bert_model.ckpt" \
    --config-file "scibert_vocab/bert_config.json" \
    --model-type "scibert" \
    --pytorch-file "scibert_scivocab_uncased.pt" \

rm "scibert_vocab/bert_model.ckpt.meta"
rm "scibert_vocab/bert_model.ckpt.data-00000-of-00001"
rm "scibert_vocab/bert_model.ckpt.index"
rm "scibert_vocab/bert_config.json"

## BLUEBERT
cd  "pretrained_models"
mkdir "bluebert_vocab"
wget https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/NCBI-BERT/NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip -O "NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip"
unzip NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip -d "bluebert_vocab"
rm "NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip"

python convert_tf_to_pt.py \
    --tf-path-model "bluebert_vocab/bert_model.ckpt" \
    --config-file "bluebert_vocab/bert_config.json" \
    --model-type "bluebert" \
    --pytorch-file "bluebert_uncased.pt" \

rm "bluebert_vocab/bert_model.ckpt.meta"
rm "bluebert_vocab/bert_model.ckpt.data-00000-of-00001"
rm "bluebert_vocab/bert_model.ckpt.index"
rm "bluebert_vocab/bert_config.json"

## BIOBERT
cd  "pretrained_models"
mkdir "biobert_vocab"
wget https://github.com/naver/biobert-pretrained/releases/download/v1.1-pubmed/biobert_v1.1_pubmed.tar.gz -O "biobert_v1.1_pubmed.tar.gz"
tar xvf biobert_v1.1_pubmed.tar.gz
rm "biobert_v1.1_pubmed.tar.gz"
mv "biobert_v1.1_pubmed/vocab.txt" "biobert_vocab/vocab.txt"
mv "biobert_v1.1_pubmed/model.ckpt-1000000.meta" "biobert_vocab/model.ckpt-1000000.meta"
mv "biobert_v1.1_pubmed/model.ckpt-1000000.data-00000-of-00001" "biobert_vocab/model.ckpt-1000000.data-00000-of-00001"
mv "biobert_v1.1_pubmed/model.ckpt-1000000.index" "biobert_vocab/model.ckpt-1000000.index"
mv "biobert_v1.1_pubmed/bert_config.json" "biobert_vocab/bert_config.json"
rm -r "biobert_v1.1_pubmed/"

python convert_tf_to_pt.py \
    --tf-path-model "biobert_vocab/model.ckpt-1000000" \
    --config-file "biobert_vocab/bert_config.json" \
    --model-type "biobert" \
    --pytorch-file "biobert_base_pubmed.pt" \

rm "biobert_vocab/model.ckpt-1000000.meta"
rm "biobert_vocab/model.ckpt-1000000.data-00000-of-00001"
rm "biobert_vocab/model.ckpt-1000000.index"
rm "biobert_vocab/bert_config.json"

## ROBERTA
cd  "pretrained_models"	
wget https://dl.fbaipublicfiles.com/fairseq/models/roberta.base.tar.gz -O "roberta.base.tar.gz"
tar xvf roberta.base.tar.gz
rm "roberta.base.tar.gz"
mv "roberta.base/dict.txt" "dict.txt"
mv "roberta.base/model.pt" "model.pt"
mv "roberta.base/NOTE" "NOTE"
rm -r "roberta.base/"

mkdir "roberta"
wget -N 'https://dl.fbaipublicfiles.com/fairseq/gpt2_bpe/encoder.json' -O "roberta/encoder.json"
wget -N 'https://dl.fbaipublicfiles.com/fairseq/gpt2_bpe/vocab.bpe' -O "roberta/vocab.bpe"
wget -N 'https://dl.fbaipublicfiles.com/fairseq/gpt2_bpe/dict.txt' -O "roberta/ict.txt"