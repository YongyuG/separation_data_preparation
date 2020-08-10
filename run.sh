#!/bin/bash

input_dir=/home/yongyug/data/timit #Dataset files
output_dir=/home/yongyug/2020_workspace/test_sep_make #output data dir, all output will be here
nums_files=10 #numbers of training set we want for training
state=train #Train for training and cross validation, test for inference
use_active=True
stage=0

if [ ! -d $output_dir ];then
	mkdir $output_dir
else
	echo "$output_dir existed"
fi

if [ $stage -le 1 ];then

	if [ -d $output_dir"/""audio" ];then
		rm -rf $output_dir"/""audio"
	fi
	if [ -d $output_dir"/""text" ];then
		rm -rf $output_dir"/""text"
	fi
	

	#Delete folder "audio" and "ext" because each time run create_inital_mixtures.py
       	#  will generate new wav pairs for mixtures, so we need to remove the old folders.
	#  (This process can be done in python if necessary)

	
	python create_inital_mixtures.py --input_dir $input_dir --output_dir $output_dir --nums_files $nums_files --state $state

fi

if [ $stage -le 2 ];then

	python create_mixtures.py --data_dir $output_dir --state $state --use_active $use_active

fi

if [ $stage -le 3 ];then

	python create_good_scp.py --data_dir $output_dir

fi

#TODO
#Will update STFT, CMVN as soon as possible.
