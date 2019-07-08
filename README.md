# methCancer-gen: a DNA methylome dataset generator for user-specified cancer type based on conditional variational autoencoder
methCancer-gen is a deep neural network-based tool for generating DNA methylome dataset based on a user-specified cancer-type. With the matrix of DNA methylation beta values and matched cancer type information as input, the methCancer-gen approximates the underlying distribution model of the input data. After model training, methylation beta value for the specified cancer type can be generated as output. methCancer-gen can address the lack of DNA methylation data and enhance efficiency in cancer related research.

![Figure](https://github.com/cbi-bioinfo/methCancer-gen/blob/master/cancer_generator.jpg?raw=true)

## Requirements
* Tensorflow (>= 1.8.0)
* Python (>= 2.7)
* Python packages : numpy, pandas

## Usage
Clone the repository or download source code files.

## Preprocessing

* Reference: ./preprocessing/

1. Prepare or edit **"cancer_type_info.csv"** file having **(1) cancer types to generate dataset** and **(2) matrix of DNA methylation beta value dataset file path** for each cancer. We recommend to generate dataset in 25 cancer types whose accuracies were validated in our manuscript using TCGA data as training dataset. (They are listed in "cancer_type_info.csv" file.) The file should contain the headers and follow the format :

```
cancer_type,datafile
BLCA,BLCA_TP.csv
BRCA,BRCA_TP.csv
CESC,CESC_TP.csv
COAD,COAD_TP.csv
...
```

Each data file should contain matrix of DNA methylation beta value, where each row and column represent **CpG site** and **sample ID**, respectively :

```
cpg,sample_1,sample_2,...,sample_n
cg00000029,0.249737,0.464333,...,0.061501
cg00000165,0.347463,0.115849,...,0.216793
cg00000236,0.917430,0.881644,...,0.908840
...
```

2. Use **"run_preproc.sh"** to perform preprocessing.

## Generating DNA methylome dataset for given cancer type

* Reference: ./methCancer_gen/

1. Prepare or edit **"sample_info.csv"** file having **(1) cancer types to generate dataset** and **(2) number of samples to generate for each cancer**. Cancer type should be in same order listed in preprocessing step. The file should contain the headers and follow the format : 
```
cancer_type,sample_num
BLCA,100
BRCA,100
CESC,100
COAD,100
...
```

2. Use **"run_methCancer_gen.sh"** to generate DNA methylaion dataset for user-specified cancer types. 
3. You can get the final output **"Generated_dataset_from_methCancer_gen.csv"**.

## Contact
If you have any question or problem, please send an email to **miniymay@sookmyung.ac.kr**
