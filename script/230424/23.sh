#!/bin/bash

cd ~/chatnvl/script/230424

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_eval \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/35ca52301fbedee885b0838da5d15b7b47faa37c \
    --dataset koikake_all_test \
    --dataset_dir ../../data \
    --output_dir all_230424_none_eval_koikake \
    --overwrite_cache \
    --per_device_eval_batch_size 8 \
    --max_samples 100 \
    --predict_with_generate

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_eval \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/35ca52301fbedee885b0838da5d15b7b47faa37c \
    --dataset alpaca_gpt4_zh \
    --dataset_dir ../../data \
    --output_dir all_230424_none_eval_alpaca \
    --overwrite_cache \
    --per_device_eval_batch_size 8 \
    --max_samples 100 \
    --predict_with_generate
