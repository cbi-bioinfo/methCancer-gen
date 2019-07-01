import sys
import pandas as pd

label_temp = []
label_tf = []
final_label = []

label_info_file = sys.argv[1]
label_info_df = pd.read_csv(label_info_file)
cancer_type = label_info_df["cancer_type"].values.tolist()
sample_num = label_info_df["sample_num"].values.tolist()

for k in range(len(cancer_type)) :
	for j in range(len(cancer_type)) :
		if k == j :
			label_temp.append(1)
		else :
			label_temp.append(0)
	label_tf.append(label_temp)
	label_temp = []


j = 0
for num in sample_num :
	for i in range(num) :
		final_label.append(label_tf[j])
	j = j + 1

final_label = pd.DataFrame(final_label, columns = cancer_type)
final_label.to_csv("label_for_sample_to_generate.csv", mode = "w", index = False, na_rep = "NA")
