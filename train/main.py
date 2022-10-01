import data
import model
import train
import sys
import argparse
import pandas as pd

def main():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default = 'bert-base-uncased')
    parser.add_argument('--lr', type = float, default=0.00005)
    parser.add_argument('--epochs', type = int, default=5)
    parser.add_argument('--train_csv', type = str, default='./data/train.csv')

    args = parser.parse_args()
    model_name = args.model_name
    lr = args.lr
    epochs = args.epochs

    df = pd.read_csv(args.train_csv)
    df = data.data_preprocess(df, 'text', 'sentiment', 3, {'negative':0, 'neutral':1, 'positive':2})
    train_df, val_df = data.split_data(df)
    train_dataset, val_dataset = data.prep_data(train_df), data.prep_data(val_df)
    
    model = model.TwitterSentimentModel(args.model_name)
    model.cuda()

    model_trainer = train.SentimentTrainer(5, 0.000005)
    model_trainer.train(model, train_dataset, val_dataset)
    
