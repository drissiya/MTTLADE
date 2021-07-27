#!/usr/bin/env bash


python ade_extraction/ade_se.py \
  --dataset "tac" \
  --predicted_rel_json_path checkpoint/tacsource_test_scores_8.json \
  --gold_rel_json_path data/canonical_data/bert_uncased_lower/tacsource_test.json \
  
python experiments/predict_prepro.py \
  --dataset "tac" \
  
python ade_prepro_std.py \
  --do_lower_case \
  --root_dir "data/canonical_data" \
  --task_def "ade_task_def.yml" \
  --model-type "scibert" \
  
python predict.py \
  --init_checkpoint pretrained_models/scibert_scivocab_uncased.pt \
  --task_def ade_task_def.yml \
  --model_ckpt checkpoint/model_8.pt \
  --test_datasets "tacsource,tacrelation" \

python ade_extraction/ade_att_re.py \
  --dataset "tac" \
  --predicted_json_path checkpoint/tacrelation_pred_scores.json \
  --gold_json_path data/canonical_data/bert_uncased_lower/tacrelation_test.json \
  --gold_xml_dir data/ADR/TAC/gold_xml \
  --guess_xml_dir data/ADR/TAC/guess_xml \