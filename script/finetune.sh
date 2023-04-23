#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_train \
    --dataset koikake_yui_train \
    --dataset_dir ../data \
    --finetuning_type lora \
    --output_dir yui_230423_lora_last3_mlp_5e_5 \
    --overwrite_cache \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 5e-5 \
    --weight_decay 1e-4 \
    --num_train_epochs 5.0 \
    --lora_target 25.mlp.dense_h_to_4h,25.mlp.dense_4h_to_h,26.mlp.dense_h_to_4h,26.mlp.dense_4h_to_h,27.mlp.dense_h_to_4h,27.mlp.dense_4h_to_h \
    --plot_loss \
    --fp16
