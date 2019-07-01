import sys
import numpy as np
import pandas as pd
from pandas import DataFrame as df

group_num = sys.argv[1]
group_num = int(group_num)

for i in range(group_num) :
	filename = "generation_split_num_" + str(i) + ".csv"
	data = pd.read_csv(filename)
	
	if i == 0 :
		temp = data
	else :
		temp = pd.concat([temp, data], axis = 1)

temp.to_csv("Generated_dataset_from_methCancer_gen.csv", mode = 'w', index = False)
