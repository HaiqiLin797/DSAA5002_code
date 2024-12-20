import logging
import torch
from snorkel.utils import probs_to_preds
from benchmark.dataset import load_dataset
from benchmark._logging import LoggingHandler
from benchmark.endmodel import MLPModel
from benchmark.endmodel import BertClassifierModel
from benchmark.labelmodel import MajorityVoting
from benchmark.labelmodel import Snorkel
from copylabels import read_labels_from_file, write_labels_to_file

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
logger = logging.getLogger(__name__)

#### Load dataset 
dataset_home = '/hpc2hdd/home/hlin797/wrench-main/datasets'
data = 'cdr' #'Bioresponse'
#### Extract data features using pre-trained BERT model and cache it
extract_fn = 'bert'
model_name = '/hpc2hdd/home/hlin797/wrench-main/pretrained_model/bert'
train_data, valid_data, test_data = load_dataset(dataset_home, data, extract_feature=False, extract_fn=extract_fn,
                                                 cache_name=extract_fn, model_name=model_name)

#### Generate soft training label via a label model
#### The weak labels provided by supervision sources are alreadly encoded in dataset object
#label_model = MajorityVoting()
label_model = Snorkel()
#print(train_data.n_class)
print(train_data.weak_labels)
label_model.fit(train_data,valid_data,y_valid=None)
soft_label = label_model.predict_proba(train_data)

hard_label = probs_to_preds(soft_label) 
l=0
for i in range(0,len(hard_label)):
    if hard_label[i]==train_data.labels[i]:
        l+=1
print(l/len(hard_label))

write_labels_to_file(hard_label, 'imdb_snorkel.txt')

