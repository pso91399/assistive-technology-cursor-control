#!/bin/bash 	#dl04
python main.py \
	--root_path ./\
	--video_path datasets/ipn \
	--annotation_path annotation_ipnGesture/ipnall_but_None.json \
	--result_path results_ipn \
	--dataset ipn \
	--sample_duration 32 \
    --learning_rate 0.01 \
    --model resnext \
	--model_depth 101 \
	--resnet_shortcut B \
	--batch_size 32 \
	--n_classes 13 \
	--n_finetune_classes 13 \
	--n_threads 16 \
	--checkpoint 1 \
	--modality RGB \
	--train_crop random \
	--n_val_samples 1 \
	--test_subset test \
    --n_epochs 100 \
    --store_name ipnClfRs_jes32r_b32 \
	--no_cuda
	#--pretrain_path report_ipn/jester_resnext_101_RGB_32.pth \
	#--pretrain_dataset jester \