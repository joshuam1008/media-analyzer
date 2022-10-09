import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split
import re

class TwitterSentimentDataset(Dataset):
    def __init__(self, text, polarity=None, max_len=64, model_name="bert-base-uncased"):
        self.text = text
        self.polarity = polarity
        self.max_len = max_len
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        input = self.tokenizer.encode_plus(
            text=self.text[index],
            add_special_tokens=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt",
            truncation=True,
            return_attention_mask=True,
        )
        if self.polarity is not None:
            output = self.polarity[index]
            return (
                torch.LongTensor(input["input_ids"]),
                torch.LongTensor(input["attention_mask"]),
                torch.FloatTensor(output),
            )
        else:
            return torch.LongTensor(input["input_ids"]), torch.LongTensor(
                input["attention_mask"]
            )


def data_preprocess(df, text_col, label_col, num_labels, label_encodings=None):
    if df is None:
        raise Exception('df must be DataFrame, not None')
    if label_col not in df.columns:
        raise Exception(str(label_col) + ' not in dataframe columns')

    if text_col not in df.columns:
        raise Exception(str(text_col) + ' not in dataframe columns')

    if label_encodings is not None:
        if len(label_encodings.keys()) == num_labels:
            df[label_col] = df[label_col].apply(lambda x: label_encodings[x])
        else:
            raise Exception('Length of label_encoding does not match number of labels')

    df[text_col] = df[text_col].apply(lambda x: re.sub(r"@\w*", "", str(x)).strip())

    def build_list(x):
        res = [0 for i in range(num_labels)]
        res[x] = 1.0
        return res

    df[label_col] = df[label_col].apply(lambda x: build_list(x))
    return df


def split_data(df):
    train, val = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
    return train, val


def prep_data(df, model_name):
    dataset = TwitterSentimentDataset(
        df["text"].tolist(), df["sentiment"].tolist(), model_name=model_name
    )
    dataset = DataLoader(
        dataset,
        batch_size=64,
        num_workers=2,
        shuffle=True,
        pin_memory=False,
        drop_last=False,
    )
    return dataset
