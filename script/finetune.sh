#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python ../chatglm-tuning/finetune.py \
    --do_train \
    --dataset belle_multiturn,koikake_yui_train \
    --dataset_dir ../data \
    --finetuning_type lora \
    --output_dir yui_230420_lora \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --max_train_samples 10000 \
    --learning_rate 1e-3 \
    --num_train_epochs 2.0 \
    --fp16
