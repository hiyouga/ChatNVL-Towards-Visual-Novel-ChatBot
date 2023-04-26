#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_train \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/35ca52301fbedee885b0838da5d15b7b47faa37c \
    --dataset koikake_yui_train \
    --dataset_dir ../data \
    --finetuning_type lora \
    --output_dir yui_230425_lora_full \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-4 \
    --num_train_epochs 3.0 \
    --lora_target 25.attention.query_key_value,26.attention.query_key_value,27.attention.query_key_value \
    --plot_loss \
    --fp16
