import logging
import torch
import copy
from benchmark.dataset import load_dataset
from benchmark._logging import LoggingHandler
from benchmark.endmodel import MLPModel
from benchmark.labelmodel import MajorityVoting
from benchmark.endmodel import BertClassifierModel
from benchmark.labelmodel import Snorkel
from snorkel.utils import probs_to_preds
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np

def kmeans_seperate_label(train_data):
    
    matrix = train_data.weak_labels
    transposed_matrix = list(zip(*matrix))
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(transposed_matrix)
    clusters = kmeans.labels_

# 分别存储属于不同簇的列号
    cluster_1_columns = [i for i, cluster in enumerate(clusters) if cluster == 0]
    cluster_2_columns = [i for i, cluster in enumerate(clusters) if cluster == 1]

    print("Cluster 1 columns:", cluster_1_columns)
    print("Cluster 2 columns:", cluster_2_columns)

    return cluster_1_columns,cluster_2_columns
def split_weak_labels(dataset):
    gen_data = copy.deepcopy(dataset)
    dis_data = copy.deepcopy(dataset)
    n_weak_labels = len(gen_data.weak_labels[0])
    #cluster = kmeans_seperate_label(dataset)
    for i in range(0,len(dataset)):
        gen_data.weak_labels[i]=dataset.weak_labels[i][0:int(n_weak_labels/2)]
        dis_data.weak_labels[i]=dataset.weak_labels[i][int(n_weak_labels/2):n_weak_labels]

    return gen_data,dis_data
def filter_invalid_data(dataset, validity_list):
    valid_indices = [i for i, validity in enumerate(validity_list) if validity == 1]
    valid_dataset = dataset.create_subset(valid_indices)
    return valid_dataset

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
logger = logging.getLogger(__name__)

#### Load dataset 
dataset_home = '/hpc2hdd/home/hlin797/wrench-main/datasets'
data = 'sms' #'Bioresponse'

#### Extract data features using pre-trained BERT model and cache it
extract_fn = 'bert'
model_name = '/hpc2hdd/home/hlin797/wrench-main/pretrained_model/bert'
train_data, valid_data, test_data = load_dataset(dataset_home, data, extract_feature=1, extract_fn=extract_fn,
                                                 cache_name=extract_fn, model_name=model_name)

#### Generate soft training label via a label model
#### The weak labels provided by supervision sources are alreadly encoded in dataset object
hard_dis_label = []

with open('labeling/lFs_sms_snorkel_llm_discriminator_1_keywords_0.txt', 'r', encoding='utf-8') as file:
#with open('new_file.txt', 'r', encoding='utf-8') as file:
    # 逐行读取并打印内容
    last_line_num = 0
    for line in file:
        line = line.strip('\n')
        line_num= int(line.split(':')[0].strip(' '))
        if line_num != 0:
            if line_num!=last_line_num+1:
                print(line_num)
                print(last_line_num)
                print("kkkkkkk")
                for i in range(last_line_num+1,line_num):
                    hard_dis_label.append(-1)
        hard_dis_label.append(int(line[-1]))
        last_line_num = line_num


print(len(hard_dis_label))

hard_gen_label = []
with open('labeling/sms_snorkel_883.txt', 'r', encoding='utf-8') as file:
    # 逐行读取并打印内容
    for line in file:
        line = line.strip('\n')
        hard_gen_label.append(int(line[-1]))

#caculate the gen-dis data pass rate
validity_list=[]
gaws_label=[]
k=0
l=0

for i in range(0,len(hard_dis_label)):
    if train_data.labels[i]==hard_dis_label[i]:
        k+=1
print(k/len(hard_dis_label))

k=0

for i in range(0,len(hard_dis_label)):
    if hard_gen_label[i]==hard_dis_label[i]:
        k+=1
        validity_list.append(1)
        gaws_label.append(hard_gen_label[i])
    else:
        validity_list.append(0)
print(k/len(hard_gen_label))


gaws_data = filter_invalid_data(train_data, validity_list)

for i in range(0,len(gaws_data)):
    if gaws_data.labels[i]==gaws_label[i]:
        l+=1
print(l/len(gaws_label))


print(gaws_data)

#### Train a MLP classifier with soft label
device = torch.device('cuda:0')
n_steps = 10000
batch_size = 128
test_batch_size = 1000 
patience = 100
evaluation_step = 100
target='acc'
#target='f1_binary'

print(len(gaws_label))
'''
model = MLPModel(n_steps=n_steps, batch_size=batch_size, test_batch_size=test_batch_size)
history = model.fit(dataset_train=gaws_data, dataset_valid=valid_data, y_train=gaws_label, 
                   device=device, metric=target, patience=patience, evaluation_step=evaluation_step)
'''

#### Evaluate the trained model
#metric_value = model.test(test_data, target)


#### We can also train a MLP classifier with hard label
#model = BertClassifierModel(n_steps=n_steps, batch_size=batch_size, test_batch_size=test_batch_size,model_name = '/hpc2hdd/home/hlin797/wrench-main/pretrained_model/bert')
model = BertClassifierModel(model_name='/hpc2hdd/home/hlin797/wrench-main/pretrained_model/bert')
model.fit(dataset_train=gaws_data, dataset_valid=valid_data, y_train=gaws_label, 
        device=device, metric=target, patience=patience, evaluation_step=evaluation_step)


#### Evaluate the trained model
metric_value = model.test(test_data, target)
print(metric_value)