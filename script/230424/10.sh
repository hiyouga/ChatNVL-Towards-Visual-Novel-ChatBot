#!/bin/bash

cd ~/chatnvl/script/230424

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_train \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/35ca52301fbedee885b0838da5d15b7b47faa37c \
    --dataset koikake_all_train,belle_multiturn \
    --dataset_dir ../../data \
    --finetuning_type p_tuning \
    --output_dir all_230424_p_tuning_yes \
    --overwrite_cache \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --lr_scheduler_type cosine \
    --logging_steps 20 \
    --save_steps 2000 \
    --learning_rate 1e-5 \
    --max_samples 10000 \
    --num_train_epochs 10.0 \
    --plot_loss \
    --fp16

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_eval \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/35ca52301fbedee885b0838da5d15b7b47faa37c \
    --dataset koikake_all_test \
    --dataset_dir ../../data \
    --checkpoint_dir all_230424_p_tuning_yes \
    --output_dir all_230424_p_tuning_yes_eval_koikake \
    --overwrite_cache \
    --per_device_eval_batch_size 8 \
    --max_samples 100 \
    --predict_with_generate

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/finetune.py \
    --do_eval \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/35ca52301fbedee885b0838da5d15b7b47faa37c \
    --dataset alpaca_gpt4_zh \
    --dataset_dir ../../data \
    --checkpoint_dir all_230424_p_tuning_yes \
    --output_dir all_230424_p_tuning_yes_eval_alpaca \
    --overwrite_cache \
    --per_device_eval_batch_size 8 \
    --max_samples 100 \
    --predict_with_generate
