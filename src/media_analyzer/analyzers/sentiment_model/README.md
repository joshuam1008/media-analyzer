# Sentiment Analysis Model Training
This directory is responsible for training the sentiment analysis model used in the twitter stream.  This README will explain how to train and deploy the models for this project.

# Requirements
- [PyTorch](https://pytorch.org/) (An open source deep learning platform) 
- [sklearn](scikit-learn.org) (Simple and efficient tools for predictive data analysis)
- [Numpy](https://numpy.org) (Support for large, multi-dimensional arrays and matrices)
- [Pandas](https://pandas.pydata.org/) (A fast, powerful, flexible and easy to use open source data analysis)

# Table Of Contents
-  [How it works](#how-it-works)
-  [Future Work](#future-work)
-  [Contributing](#contributing)

# How it works 
In this solution we are using a pretrained language model (BERT in this case) and training a classification layer on top of it to make predictions across three different classes.  The dataset used to train the deep model can be found here: https://www.kaggle.com/competitions/tweet-sentiment-extraction/data?select=train.csv.  One can train a model using ```python train/main.py --epochs=[Number of training epochs] --lr=[Learning rate] --train_csv=[Training data directory] --model_name=[Pretrained model name from huggingface.co]```

IMPORTANT: The name of the model used in training must be used in src/inferece.py because the same architecture must be used to load weights.


# Future Work
Some future work to this model could include hyperparameter tuning, shrinking the mdoel for faster inference, testing other preprocessing techniquse to remove irrelevant information such as links, and potentially add more predictive models such as bot detection.  The model could also be improved by including more sentiment options such as partially positive and partially negative.

# Contributing
All contributions are welcome such that the same coding guidelines are met.




