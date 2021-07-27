# MTTLADE: A multi-task transfer learning-based method for adverse drug events extraction 
MTTLADE is a multi-task transfer learning-based method for extracting mentions of adverse drug events (ADEs) and the potential relationships among them. It converts the ADEs extraction task to a dual-task sequence labelling which includes ADEs source mention extraction (ADE-SE) and ADEs attribute-relation extraction (ADE-Att-RE) tasks. The ADE-SE task aims at extracting the source mentions that are likely related to at least one relation, while the ADE-Att-RE task consists in linking the previously identified source mentions to their target attributes and relation types by adopting a unified sequence labelling. Then, it uses the multi-task transfer learning (MTTL) based approach to process the two proposed tasks simultaneously. The MTTL adopts a shared representation obtained from the pre-trained language model learned through transformer architecture and ends up with tasks-pecific fine-tuning. This allows the MTTLADE system to yield more generalized representation across the tasks. Finally, MTTLADE produces sequences for each task from the generated model so as to extract ADEs mentions and relations.

## Datasets
We conducted experiments on two datasets:
- TAC 2017 dataset: includes 200 drug labels in XML format separated into 101 labels for the training set and 99 ones for the test set. After clone this repository, download the training set from [here](https://bionlp.nlm.nih.gov/tac2017adversereactions/), unzip the file and put the xml files to the data/ADR/TAC/train_xml folder. After getting received the gold set by the organizers, put the xml files to the data/ADR/TAC/gold_xml folder. The data/ADR/TAC/TR and data/ADR/TAC/TE folders contain the sentence boundary outcomes for training and test sets, respectively, obtained from [GENIA Sentence Splitter](http://www.nactem.ac.uk/y-matsu/geniass/).
- n2c2 2018 dataset: contains 505 discharge summaries in brat format separated into 303 for training set and 202 for testing set. You must sign the agreements from [here](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/) to request access to this dataset as well as the official script for evaluation. After clone this repository, place the train, test and guess brat files to the data/ADR/N2C2/training_20180910, data/ADR/N2C2/test and data/ADR/N2C2/test_data_Tasks1_3 folders, respectively.

Additional datasets are obtained from i2b2 2009, i2b2 2010, CoNLL 2003 and ADE corpus which are explored for the sake of comparison.

## Requirements

1. Install all dependencies needed to run this repository using the command:

```
$ pip install -r requirements.txt
```

2. Download the pre-trained model files used for MTTLADE experiments. They include BERT, BioBERT, SciBERT, BlueBERT and RoBERTa. Convert the Tensorflow BERT-based models to the Pytorch version which is used by mt-dnn. To do so, just run the following command:

```
$ bash pretrained_models/convert_tf_to_pt.sh
```


## Quick start

1. Specify the encoder_type in the ade_task_def.yml file which is used for tasks' definition. Choose one from encoder types in: SCIBERT, BIOBERT, BERT, BLUEBERT, ROBERTA.

2. Preprocess the datasets by running the ade_prepro.sh file. It converts the datasets to the canonical format using the ade_prepro.py file. Then, it preprocesses the canonical data to the mt-dnn format using the ade_prepro_std.py:

```
$ bash ade_prepro.sh
```

3. To train the MTTLADE system, you can run the train.py file:
```
$ python train.py \
  --init_checkpoint pretrained_models/scibert_scivocab_uncased.pt \
  --task_def ade_task_def.yml \
  --train_datasets "tacsource,tacrelation" \
  --test_datasets "tacsource,tacrelation" \
```
- init_checkpoint: specifies the path of the pre-trained model (SciBERT in this case)
- task_def: indicates the path of yaml file. 
- train_datasets: specifies the tasks to be learned (tacsource for ADE-SE task and tacrelation for ADE-Att-RE task). 

4. To extract the guessed mentions and relations from the test data, run the following command:
```
$ bash inference.sh
```
It includes the following files:
- ade_extraction/ade_se.py: extracts source mentions and generates contexts for positive ones.
- predict.py: predicts sequences for ADE-Att-RE task.
- ade_extraction/ade_att_re.py: extracts target attributes and relation types.

After the program is finished, the guess xml files will be generated in the data/ADR/TAC/guess_xml folder for TAC 2017 dataset. 

5. To evaluate MTTLADE on TAC 2017 dataset, run evaluate.py file which includes the official script for this challenge:
```
$ python evaluate.py "data/ADR/TAC/gold_xml" "data/ADR/TAC/guess_xml"
```

The same procedure can be used for n2c2 2018 dataset.

## Citation 

```
@article{El_allaly_2021,
	doi = {10.1016/j.ipm.2020.102473},
	year = 2021,
	volume = {58},
	pages = {102473},
	author = {Ed-drissiya El-allaly and Mourad Sarrouti and Noureddine En-Nahnahi and Said Ouatik El Alaoui},
	title = {{MTTLADE}: A multi-task transfer learning-based method for adverse drug events extraction},
	journal = {Information Processing {\&} Management}
}
```

## Acknowledgements

We are very grateful to the authors of [mt-dnn](https://github.com/namisan/mt-dnn) to make the code publicly available. We are also grateful to the TAC 2017 ADR challenge organizers and the n2c2 challenge organizers who provided us the datasets used to evaluate this work.

