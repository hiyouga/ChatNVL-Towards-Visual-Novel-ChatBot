#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python ~/chatglm_tuning/src/train_rm.py \
    --do_train \
    --model_name_or_path ~/.cache/huggingface/hub/models--THUDM--chatglm-6b/snapshots/a8ede826cf1b62bd3c78bdfb3625c7c5d2048fbd \
    --dataset comparison_gpt4_en,comparison_gpt4_zh \
    --dataset_dir ~/chatglm_tuning/data \
    --finetuning_type lora \
    --output_dir reward_model_230510_en_zh \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 1000 \
    --learning_rate 1e-5 \
    --weight_decay 1e-5 \
    --num_train_epochs 1.0 \
    --lora_target query_key_value \
    --source_prefix 现在你将扮演结衣，模拟学长和结衣的对话。结衣，你是御影浜学校的少女，喜欢学长、绘本、安静的地方、花和小动物。请根据角色性格特点，补全对话，下面是对话片段。 \
    --plot_loss \
    --fp16
