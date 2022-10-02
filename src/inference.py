import torch
from torch.utils.data import DataLoader
import sys
sys.path.insert(0, '../')
from train.model import TwitterSentimentModel
from train.data import TwitterSentimentDataset
import numpy as np
import pandas as pd
import time

class SentimentPredictor():
    def __init__(self, model_dir):
        self.model = TwitterSentimentModel()
        self.model.cuda()
        self.model.load_state_dict(torch.load(model_dir))

    def read_data(self, data):
        '''
        Load the data into the cuda device
        '''
        return tuple(x.cuda() for x in data)

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
        data_sample *= 2
        data_input = TwitterSentimentDataset(text=data_sample)
        data_input = DataLoader(data_input, batch_size=16, num_workers=1, shuffle=True, pin_memory=False, drop_last=False)
        pair = {0:'NEGATIVE', 1:'NEUTRAL', 2:'POSITIVE'}
        predicts = []
        for (X, mask) in data_input:
            data = self.read_data((X, mask))
            preds = self.model(data[0].squeeze(), data[1].squeeze())
            preds = self.get_pred(preds.detach().cpu().numpy())
            for p in preds:
                predicts.append(pair[p])

        return predicts[::2]