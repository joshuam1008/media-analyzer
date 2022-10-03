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

class SentimentPredictor():
    def __init__(self, model_dir):
        self.model = TwitterSentimentModel(model_name='prajjwal1/bert-mini')
        self.model.cpu()
        self.model.load_state_dict(torch.load(model_dir))

    def read_data(self, data):
        '''
        Load the data into the cuda device
        '''
        return tuple(x.cpu() for x in data)

    def get_pred(self, data):
        '''
        Set the prediction to 1 if the prediction exceeds 0.5 probability
        '''
        results = []
        for d in data:
            results.append(np.argmax(d))
        return results

    def make_prediction(self, data_sample):
        '''
        Run the model on a data sample
         - data_sample: A list of tweets to build inference on
        returns: A list of enumerated values (NEGATIVE, NEUTRAL, POSITIVE)
        '''

        tokenizer = AutoTokenizer.from_pretrained('prajjwal1/bert-mini')
        pair = {0:'NEGATIVE', 1:'NEUTRAL', 2:'POSITIVE'}
        predicts = []
        for data in tqdm(data_sample):
            input = tokenizer.encode_plus(text = data,
                                            add_special_tokens=True,
                                            padding='max_length',
                                            max_length = 64,
                                            return_tensors='pt',
                                            truncation=True,
                                            return_attention_mask=True)

  
            preds = self.model(input['input_ids'].cpu(), input['attention_mask'].cpu()).detach().numpy().ravel()
            p = np.argmax(preds)
            predicts.append(pair[p])
        return predicts