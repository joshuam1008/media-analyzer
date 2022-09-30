import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.metrics import accuracy_score

def read_data(data):
  '''
  Load the data into the cuda device
  '''
  return tuple(x.cuda() for x in data[0:-1]), data[-1].cuda()

def get_pred(data):
  '''
  Set the prediction to 1 if the prediction exceeds 0.5 probability
  '''
  results = []
  for d in data:
    temp = [0 for i in range(3)]
    temp[np.argmax(d)] = 1.0
    results.append(temp)
    return results

def train(model, train_loader, val_loader, epochs, learning_rate):
  optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
  loss_fn = torch.nn.CrossEntropyLoss()

  loss_saves = []
  accuracy_saves = []

  for e in range(epochs):
    tbar = tqdm(train_loader)
    loss_temp = []
    acc_temp = []
    for batch, (X, mask, Y) in enumerate(tbar):
      data, target = read_data((X, mask, Y))
      optimizer.zero_grad()
      preds = model(data[0].squeeze(), data[1].squeeze())
      loss = loss_fn(preds, target)
      loss.backward()
      optimizer.step()

      loss_temp.append(loss.detach().cpu().numpy().ravel())

      predicts = get_pred(preds.detach().cpu().numpy())
      acc = accuracy_score(predicts, target.detach().cpu().numpy())
      acc_temp.append(acc)

      tbar.set_description('Epoch: %i  Loss: %f  Accuracy %f' % (e, np.round(np.mean(loss_temp), 4), np.round(np.mean(acc_temp), 4)))

    model.eval()
    val_loss_temp = []
    val_acc_temp = []
    vbar = tqdm(val_loader)
    with torch.no_grad():
      for batch, (X, mask, y) in enumerate(vbar):
        data, target = read_data((X, mask, y))
        preds = model(data[0].squeeze(), data[1].squeeze())
        loss = loss_fn(preds, target)
        val_loss_temp.append(loss.detach().cpu().numpy().ravel())
        predicts = get_pred(preds.detach().cpu().numpy())
        acc = accuracy_score(predicts, target.detach().cpu().numpy())
        val_acc_temp.append(acc)
        vbar.set_description('Epoch: %i  Val Loss: %f  Val Accuracy %f' % (e, np.round(np.mean(val_loss_temp), 4), np.round(np.mean(val_acc_temp), 4)))
    
    torch.save(model.state_dict(), '/content/checkpoints/' + str(e) + '_checkpoint.pt')