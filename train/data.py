import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer
from sklearn.model_selection import test_train_split
import re

class TwitterSentimentDataset(Dataset):
  def __init__(self,
               text,
               polarity,
               max_len=64,
               model_name = 'bert-base-uncased'):
    self.text = text
    self.polarity = polarity
    self.max_len = max_len
    self.tokenizer = BertTokenizer.from_pretrained(model_name)
  
  def __len__(self):
    return len(self.text)

  def __getitem__(self, index):
    input = self.tokenizer.encode_plus(text = self.text[index],
                                        add_special_tokens=True,
                                        padding='max_length',
                                        max_length = self.max_len,
                                        return_tensors='pt',
                                        truncation=True,
                                        return_attention_mask=True)
    output = self.polarity[index]
    return torch.LongTensor(input['input_ids']), torch.LongTensor(input['attention_mask']), torch.FloatTensor(output)

def data_preprocess(df, text_col, label_col, num_labels, label_encodings=None):
  if label_encodings is not None:
    df[label_col] = df[label_col].apply(lambda x: label_encodings[x])
  df[text_col] = df[text_col].apply(lambda x: re.sub('@\w*', '', str(x)).strip())
  def build_list(x):
    res = [0 for i in range(num_labels)]
    res[x] = 1.0
    return res

  df[label_col] = df[label_col].apply(lambda x: build_list(x))
  return df

def prep_data(df):
    dataset = TwitterSentimentDataset(df['text'].tolist(), df['sentiment'].tolist())
    dataset = DataLoader(dataset, batch_size=64, num_workers=2, shuffle=True, pin_memory=False, drop_last=False)
    return dataset

