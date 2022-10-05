import torch
from torch.utils.data import DataLoader
import sys
sys.path.insert(0, '../')
from train.model import TwitterSentimentModel
from train.data import TwitterSentimentDataset
from transformers import AutoTokenizer
import numpy as np
import pandas as pd
import time
from tqdm import tqdm

model_name = 'prajjwal1/bert-mini'
model_dir = '../train/checkpoints/TwitterSentimentModel.pt'
Sentiment = TwitterSentimentModel(model_name=model_name)
Sentiment.cpu()
Sentiment.load_state_dict(torch.load(model_dir))

def make_prediction(data_sample):
    '''
    Run the model on a data sample
        - data_sample: A list of tweets to build inference on
    returns: A list of enumerated values (NEGATIVE, NEUTRAL, POSITIVE)
    '''

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    pair = {0:'NEGATIVE', 1:'NEUTRAL', 2:'POSITIVE'}
    predicts = []
    for data in data_sample:
        input = tokenizer.encode_plus(text = data,
                                        add_special_tokens=True,
                                        padding='max_length',
                                        max_length = 64,
                                        return_tensors='pt',
                                        truncation=True,
                                        return_attention_mask=True)


        preds = Sentiment(input['input_ids'].cpu(), input['attention_mask'].cpu()).detach().numpy().ravel()
        p = np.argmax(preds)
        predicts.append(pair[p])
    return predicts