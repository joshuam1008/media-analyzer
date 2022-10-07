import torch.nn as nn
from transformers import AutoModel, AutoConfig


class TwitterSentimentModel(nn.Module):
    def __init__(self, model_name="bert-base-uncased", num_classes=3):
        super(TwitterSentimentModel, self).__init__()
        self.config = AutoConfig.from_pretrained(model_name, num_labels=num_classes)
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout1 = nn.Dropout(0.3)
        self.dropout2 = nn.Dropout(0.3)
        self.lin = nn.Linear(self.config.hidden_size, 64)
        self.relu = nn.ReLU()
        self.classifier = nn.Linear(64, num_classes)
        self.softmax = nn.Softmax(-1)

    def forward(self, input, attention_mask):
        x = self.bert(input, attention_mask)[0][:, 0, :]
        x = self.dropout1(x)
        x = self.lin(x)
        x = self.relu(x)
        x = self.dropout2(x)
        x = self.classifier(x)
        x = self.softmax(x)
        return x
