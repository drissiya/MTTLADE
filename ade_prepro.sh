#!/usr/bin/env bash


python ade_prepro.py
  --data_dir "data/ADR" \
  --output_dir "data/canonical_data" \


python ade_prepro_std.py \
  --do_lower_case \
  --root_dir "data/canonical_data" \
  --task_def "ade_task_def.yml" \
  --model-type "scibert" \