#!/bin/bash

sample_info="./sample_info.csv" #WRITE FILENAME OF SAMPLE INFO FOR GENERATION

subset_num=$(<../preprocessing/subset_num)

python make_label.py $sample_info
label_info="label_for_sample_to_generate.csv"

for ((i=0; i<$subset_num; i++))
do
 training_x="../preprocessing/trainingSet_for_generator_split_num_"$i".csv"
 training_y="../preprocessing/trainingSet_for_generator_split_num_y_"$i".csv"
 python methCancer_gen.py $training_x $training_y $label_info $i
 msg="DONE processing methCancer-gen for trainingSet "$i
 echo $msg
done

python merge_files.py $subset_num
