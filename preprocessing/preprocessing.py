import sys
import random
import numpy as np
import pandas as pd
from pandas import DataFrame as df

cancer_type_file = sys.argv[1]
cancer_type_df = pd.read_csv(cancer_type_file)
cancer_type = cancer_type_df["cancer_type"].values.tolist()
input_file_list = cancer_type_df["datafile"].values.tolist()


i = 0
j = 1
t = 0
total_delete_cpg = []
label_tf = []
label_temp = []

for k in range(len(cancer_type)) :
		for j in range(len(cancer_type)) :
			if k == j :
				label_temp.append(1)
			else :
				label_temp.append(0)
		label_tf.append(label_temp)
		label_temp = []


print("READING INPUT FILES TO DELETE CPGS HAVING MISSING VALUES FOR ALL SAMPLES IN EACH CANCER")
for name in cancer_type :
	raw_x = pd.read_csv(input_file_list[t], index_col = 0)
	raw_x_T = raw_x.T
	x_data_na_index = pd.isnull(raw_x_T).all(0).nonzero()[0]
	if len(x_data_na_index) != 0 :
		x_data_na_cpg = raw_x_T.columns[x_data_na_index]
		if len(total_delete_cpg) == 0 :
			total_delete_cpg = x_data_na_cpg
		else :
			total_delete_cpg = total_delete_cpg.append(x_data_na_cpg)
	t = t + 1

if len(total_delete_cpg) != 0 :
	total_delete_cpg = total_delete_cpg.unique()

t = 0
j = 1
split_data_y = []
real_y_test = []
split_data = []
split_data_with_median = []


print("SPLITTING INPUT FILES INTO MULTIPLE SUBSETS")
for name in cancer_type :
	raw_x = pd.read_csv(input_file_list[t], index_col = 0)
	print("READING " + name + " DONE")
	raw_x_T = raw_x.T
	raw_x_T = raw_x_T.drop(total_delete_cpg, axis = 1)
	cpg_num = len(raw_x_T.columns)
	iter_num = cpg_num / 10000
	last_iter_cpg_num = cpg_num % 10000
	sample_num = len(raw_x_T.index)


	for i in range(iter_num) :
		split_data_temp = raw_x_T.T[i*10000 : (i+1)*10000].T
		split_data_y_temp = []

		if j == 1 :
			split_data.append(split_data_temp)
			tp = split_data_temp.fillna(split_data_temp.median())
			split_data_with_median.append(tp)
			for label_i in range(len(split_data_temp)) :
				split_data_y_temp.append(label_tf[j-1])
			split_data_y.append(split_data_y_temp)
		else :
			split_data[i] = pd.concat([split_data[i], split_data_temp], axis = 0)
			tp = split_data_temp.fillna(split_data_temp.median())
			split_data_with_median[i] = pd.concat([split_data_with_median[i], tp], axis = 0, sort = True)
			for label_i in range(len(split_data_temp)) :
				split_data_y[i].append(label_tf[j-1])

	split_data_temp = raw_x_T.T[iter_num*10000 : cpg_num].T
	split_data_y_temp = []

	if j == 1 :
		split_data.append(split_data_temp)
		split_data_with_median.append(split_data_temp.fillna(split_data_temp.median()))
		for label_i in range(len(split_data_temp)) :
			split_data_y_temp.append(label_tf[j-1])
		split_data_y.append(split_data_y_temp)
	else :
		split_data[iter_num] = pd.concat([split_data[iter_num], split_data_temp], axis = 0)
		split_data_with_median[iter_num] = pd.concat([split_data_with_median[iter_num], split_data_temp.fillna(split_data_temp.median())], axis = 0, sort = True)

		for label_i in range(len(split_data_temp)) :
			split_data_y[iter_num].append(label_tf[j-1])

	j = j + 1
	t = t + 1


print("REMOVING OUTLIER SAMPLES IN EACH SUBSET")
for i in range(iter_num + 1) :
	split_data_y[i] = pd.DataFrame(split_data_y[i], index = split_data[i].index)
	samplenum = len(split_data[i].index)
	na_count = []

	for j in range(samplenum) :
		na_count.append(split_data[i].iloc[j].isnull().sum())

	na_count = pd.DataFrame(na_count, index = split_data[i].index)
	na_count.columns = ["count"]
	upperQ = np.percentile(na_count, 75)
	lowerQ = np.percentile(na_count, 25)
	iqr = upperQ - lowerQ
	outlier_u = na_count[na_count['count'] > upperQ + iqr*1.5].index
	outlier_l = na_count[na_count['count'] < lowerQ - iqr*1.5].index

	if len(outlier_u) != 0 :
		split_data_with_median[i] = split_data_with_median[i].drop(outlier_u, axis = 0)
		split_data_y[i] = split_data_y[i].drop(outlier_u, axis = 0)

	if len(outlier_l) != 0 :
		split_data_with_median[i] = split_data_with_median[i].drop(outlier_l, axis = 0)
		split_data_y[i] = split_data_y[i].drop(outlier_l, axis = 0)

	split_data_with_median[i].to_csv("trainingSet_for_generator_split_num_" + str(i) + ".csv", mode = 'w', index = False, na_rep = "NA")
	split_data_y[i].to_csv("trainingSet_for_generator_split_num_y_" + str(i) + ".csv", mode = 'w', index = False, na_rep = "NA")
	print("WRITING SPLIT NUMBER " + str(i) + " DONE")

print("TOTAL NUMBER OF SPLIT SUBSETS : " + str(iter_num + 1))
f = open("subset_num", 'w')
f.write("%d" % (iter_num + 1))
f.close()
