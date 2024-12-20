import logging
import torch
import copy
from wrench.dataset import load_dataset
from wrench._logging import LoggingHandler
from wrench.endmodel import MLPModel
from wrench.labelmodel import MajorityVoting
from wrench.endmodel import BertClassifierModel
from wrench.labelmodel import Snorkel
from snorkel.utils import probs_to_preds
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np
from chatgpt import llm_discriminator_sms_keywords,llm_discriminator_spouse_keywords,llm_discriminator_imdb_keywords,llm_discriminator_trec_keywords
from copylabels import read_labels_from_file, write_labels_to_file
import time
import emoji
def text_to_list(text):
    # 将文本按换行符分割成行
    lines = text.split('\n')
    # 初始化空列表
    result_list = []
    # 遍历每一行
    for line in lines:
        # 忽略空行
        if line.strip():
            # 分割每一行，得到索引和值
            if ' ' in line:
                index, value = line.split(': ')
            else:
                index, value = line.split(':')
            # 添加到结果列表
            result_list.append(value)
    return result_list

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
logger = logging.getLogger(__name__)

#### Load dataset 
dataset_home = '/hpc2hdd/home/hlin797/wrench-main/datasets'
data = 'trec' #'Bioresponse'

#### Extract data features using pre-trained BERT model and cache it
extract_fn = 'bert'
model_name = '/hpc2hdd/home/hlin797/wrench-main/pretrained_model/bert'
train_data, valid_data, test_data = load_dataset(dataset_home, data, extract_feature=False, extract_fn=extract_fn,
                                                 cache_name=extract_fn, model_name=model_name)
#read_labels = read_labels_from_file("youtube_snorkel_844.txt")

with open('/hpc2hdd/home/hlin797/wrench-main/datasets/trec/readme.txt', 'r') as file:
    # 读取文件内容
    rule = file.read()
dis_label = []
generations = ''
file_path = 'lFs_trec_snorkel_llm_discriminator_1_keywords_0.txt'
with open(file_path, 'w') as file:
    for i in range(len(train_data.examples)):
        #time.sleep(30)
        generations += ("data id " + str(i) + " : \ntext: " + emoji.demojize(train_data.examples[i]['text']) + '\n')  # pseudo label: '+str(read_labels[i])+'\n')
        #generations += ("data id " + str(i) + " : \ntext: " + emoji.demojize(train_data.examples[i]['text']) + "\n entity1:"+train_data.examples[i]['entity1'] + "\n entity2:" + train_data.examples[i]['entity2'] +'\n')  # pseudo label: '+str(read_labels[i])+'\n')#spouse
        if (i % 5 == 0 and i != 0) or i == len(train_data.examples) - 1:
            while(1):
                try:
                    print(i)
                    print(generations)
                    response = llm_discriminator_trec_keywords(generations,rule)
                    if 'error' in response:
                        error_plot = response['error']['message']
                        if 'policy' in error_plot:
                            error_label = ''
                            for j in range(0,5):
                                error_label+=f'{i-4+j}:0\n'
                            file.write(error_label)
                            generations = ''
                            break
                    content = response['choices'][0]['message']['content']
                    #print(content)
                    #dis_label += text_to_list(content)
                    file.write(content + '\n')
                    #print(dis_label)
                    generations = ''
                    break
                    #print(response.keys())
                except Exception as e:
                    print("An error occurred:", e)
                    print("Retrying after 60 seconds...")
                    time.sleep(20)

#write_labels_to_file(dis_label, 'lFs_youtube_snorkel_llm_discriminator_1_keywords.txt')

