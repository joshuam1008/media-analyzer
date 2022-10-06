import torch
from torch.utils.data import DataLoader
import sys

sys.path.insert(0, "../")
import os
from train.model import TwitterSentimentModel
from train.data import TwitterSentimentDataset
from transformers import AutoTokenizer
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import re

model_name = "prajjwal1/bert-mini"
model_dir = os.path.join(
    os.path.dirname(__file__), "../train/checkpoints/TwitterSentimentModel.pt"
)
Sentiment = TwitterSentimentModel(model_name=model_name)
Sentiment.cpu()
# only use cpu if cuda is not available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
Sentiment.load_state_dict(torch.load(model_dir, map_location=device))

tokenizer = AutoTokenizer.from_pretrained(model_name)


def make_prediction(data_sample):
    """
    Run the model on a data sample
        - data_sample: A tweet to make inference on
    returns: A dict of prediction (NEGATIVE, NEUTRAL, POSITIVE) and the cleaned text
    """
    data_sample = re.sub("@\w*", "", data_sample).strip()
    pair = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
    input = tokenizer.encode_plus(
        text=data_sample,
        add_special_tokens=True,
        padding="max_length",
        max_length=64,
        return_tensors="pt",
        truncation=True,
        return_attention_mask=True,
    )

    preds = (
        Sentiment(input["input_ids"].cpu(), input["attention_mask"].cpu())
        .detach()
        .numpy()
        .ravel()
    )
    p = np.argmax(preds)

    return {"emo": pair[p], "clean-text": data_sample}
