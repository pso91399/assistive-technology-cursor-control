#!/bin/bash
export CUDA_VISIBLE_DEVICES=0

python offline_test.py \
	--root_path ./ \
	--video_path datasets/ipn/videos/ \
	--annotation_path annotation_ipnGesture/ipnbinary.json \
	--result_path results_ipn \
	--resume_path report_ipn/ipnDet_sc8b64_resnetl-10.pth \
    --store_name ipnDet_sc8b64 \
	--modality RGB \
	--dataset ipn \
	--sample_duration 32 \
    --model resnetl \
	--model_depth 10 \
	--resnet_shortcut A \
	--batch_size 1 \
	--n_classes 2 \
	--n_finetune_classes 2 \
	--n_val_samples 1 \
	--test_subset test \
    --n_epochs 100 \
    --no_train \
    --no_val \
    --test \
	--no_cuda