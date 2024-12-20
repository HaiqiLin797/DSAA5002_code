

import requests 
import json 

def llm_discriminator_youtube_keywords( text,rule ):
  url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions" 
  headers = { 
  "Content-Type": "application/json", 
  "Authorization": "Bearer 8940819edac2467fb87a9a265e7c014543b4b616606f4f74a900d4f6c15d334c" 
  } 
  data = { 
  "model": "gpt-3.5-turbo", 
  "messages": [
    {"role": "system", "content": "you are an data annotator,Please annotate these datas, with the keywords being your significant judgment criteria."},
    {"role": "system", "content": rule},
    {"role": "system", "content": "Labels determined according to the above rules may have omissions. Please annotate the data using a different approach than the above labels."},
    {"role": "user","content":"the label 1 means spam, 0 means not,please reply to me in standard format: id:label .now you will receive data "+text},
      ], 
  "temperature":0,
  } 
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  return response.json()


def llm_discriminator_sms_keywords( text,rule ):
  url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions" 
  headers = { 
  "Content-Type": "application/json", 
  "Authorization": "Bearer 8940819edac2467fb87a9a265e7c014543b4b616606f4f74a900d4f6c15d334c" 
  } 
  data = { 
  "model": "gpt-3.5-turbo", 
  "messages": [
    {"role": "system", "content": "you are an data annotator,Please annotate these datas, with the keywords being your significant judgment criteria."},
    {"role": "system", "content": rule},
    {"role": "system", "content": "Labels determined according to the above rules may have omissions. Please annotate the data using a different approach than the above labels."},
    {"role": "user","content":"the label 1 means spam, 0 means not,please reply to me in standard format: id:label .now you will receive data "+text},
      ], 
  "temperature":0,
  } 
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  return response.json()

def llm_discriminator_spouse_keywords( text,rule ):
  url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions" 
  headers = { 
  "Content-Type": "application/json", 
  "Authorization": "Bearer 8940819edac2467fb87a9a265e7c014543b4b616606f4f74a900d4f6c15d334c" 
  } 
  data = { 
  "model": "gpt-3.5-turbo", 
  "messages": [
    {"role": "system", "content": "you are an data annotator,Please annotate these datas, with the keywords being your significant judgment criteria.This dataset is  to identify mentions of spouse relationships in a set of news articles from the Signal Media.You should classify the relationship between entity1 and entity2 in the text. "},
    {"role": "system", "content": rule},
    {"role": "system", "content": "Labels determined according to the above rules may have omissions. Please annotate the data using a different approach than the above labels."},
    {"role": "user","content":"the label 1 means spouse, 0 means not spouse,please reply to me in standard format: id:label .now you will receive data "+text},
      ], 
  "temperature":0,
  } 
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  return response.json()
def llm_discriminator_imdb_keywords( text,rule ):
  url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions" 
  headers = { 
  "Content-Type": "application/json", 
  "Authorization": "Bearer 8940819edac2467fb87a9a265e7c014543b4b616606f4f74a900d4f6c15d334c" 
  } 
  data = { 
  "model": "gpt-3.5-turbo", 
  "messages": [
    {"role": "system", "content": "you are an data annotator,Please annotate these datas, with the keywords being your significant judgment criteria.This is a dataset for binary sentiment classification containing a set of 20,000 highly polar movie reviews for training, 2,500 for validation and 2,500 for testing."},
    {"role": "system", "content": rule},
    {"role": "system", "content": "Labels determined according to the above rules may have omissions. Please annotate the data using a rules than the above rules."},
    {"role": "user","content":"the label 1 means Positive, 0 means Negative ,please reply to me in standard format: id:label .now you will receive data "+text},
      ], 
  "temperature":0
  } 
  response = requests.post(url, headers=headers, data=json.dumps(data))
  return response.json()
def llm_discriminator_trec_keywords( text,rule ):
  url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions" 
  headers = { 
  "Content-Type": "application/json", 
  "Authorization": "Bearer 8940819edac2467fb87a9a265e7c014543b4b616606f4f74a900d4f6c15d334c" 
  } 
  data = { 
  "model": "gpt-3.5-turbo", 
  "messages": [
    {"role": "system", "content": "you are an data annotator,Please annotate these datas, with the keywords being your significant judgment criteria."},
    {"role": "system", "content": rule},
    {"role": "system", "content": "Labels determined according to the above rules may have omissions. Please annotate the data using a different approach than the above labels."},
    {"role": "user","content":"the mean:label is {Description (DESC) : 0 Entity (ENTY) : 1 Human (HUM) : 2 Abbreviation(ABBR): 3 Location(LOC) : 4 Number (NUM): 5},please reply to me in standard format: id:label .now you will receive data "+text},
      ], 
  "temperature":0,
  } 
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  return response.json()