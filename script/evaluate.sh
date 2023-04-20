#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python ../chatglm-tuning/finetune.py \
    --do_eval \
    --dataset alpaca_gpt4_zh \
    --dataset_dir ../data \
    --output_dir output_eval \
    --overwrite_cache \
    --per_device_eval_batch_size 8 \
    --max_eval_samples 20 \
    --predict_with_generate
