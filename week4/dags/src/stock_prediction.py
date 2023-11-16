from datetime import timedelta, datetime
import numpy as np
import pandas as pd

import sklearn
import sklearn.preprocessing

import torch
import torch.nn as nn
import torch.optim as optim

from pykrx import stock

# ------------------------------------------------------------------

# (1) Data Config
def get_data_config():
    
    valid_set_size_percentage = 10
    test_set_size_percentage = 10
    seq_len = 20
    
    return valid_set_size_percentage, test_set_size_percentage, seq_len

# ------------------------------------------------------------------

# (2) Import Data
def get_today():
    
    dt_now = str(datetime.now().date())
    print(f'{dt_now} 기준')
    
    dt_now = ''.join(c for c in dt_now if c not in '-')
    
    return dt_now # 20230101 과 같은 형태로 변환


def get_market_fundamental():
    
    dt_now = get_today()
    
    df = stock.get_market_ohlcv("20230101", "{dt_now}", "005930")  # 2023년 1월 1일부터 오늘까지 '삼성전자' 주가
    df.columns = ['open', 'high', 'low', 'close', 'volume', 'RoC'] # 영문으로 칼럼명 변경
    
    print(df.info())
    print(df.head())
    
    df.to_csv(f'./{dt_now}_market_fundamental.csv', index=True)  
    
# ------------------------------------------------------------------
    
# (3) Proprocess Data
def normalize_data(df):
    
    dt_now = get_today()
    norm_df = df.copy()
    
    min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    norm_df['open'] = min_max_scaler.fit_transform(norm_df.open.values.reshape(-1,1))
    norm_df['high'] = min_max_scaler.fit_transform(norm_df.high.values.reshape(-1,1))
    norm_df['low'] = min_max_scaler.fit_transform(norm_df.low.values.reshape(-1,1))
    norm_df['close'] = min_max_scaler.fit_transform(norm_df['close'].values.reshape(-1,1))
    
    print(norm_df.head())
    norm_df.to_csv(f'./{dt_now}_normalized_market_fundamental.csv', index=True)
    
    return norm_df
  

def get_data_size():
    

  
def split_data(df):
    
    valid_set_size_percentage, test_set_size_percentage, seq_len = get_data_config()
    data_raw = df.values
    data = []
    
    # 기존 데이터의 배치(batch)화
    for index in range(len(data_raw) - seq_len):
        data.append(data_raw[index: index + seq_len])
    data = np.array(data);
    
    valid_set_size = int(np.round(valid_set_size_percentage/100*data.shape[0])); 
    test_set_size = int(np.round(test_set_size_percentage/100*data.shape[0])); 
    train_set_size = data.shape[0] - (valid_set_size + test_set_size);

    print(data)
    x_train = data[:train_set_size,:-1,:]
    y_train = data[:train_set_size,-1,:]

    x_valid = data[train_set_size:train_set_size+valid_set_size,:-1,:]
    y_valid = data[train_set_size:train_set_size+valid_set_size,-1,:]

    x_test = data[train_set_size+valid_set_size:,:-1,:]
    y_test = data[train_set_size+valid_set_size:,-1,:]

    return [x_train, y_train, x_valid, y_valid, x_test, y_test]


def remove_columns(df):
    
    df.drop(['RoC'],1,inplace=True)
    df.drop(['volume'],1,inplace=True)

    cols = list(df.columns.values)
    print('df_stock.columns.values = ', cols)
    
    return df

# ------------------------------------------------------------------

# (4) Model 
def get_model_config():
    
    _, _, seq_len = get_data_config()

    n_steps = seq_len - 1
    n_inputs = 4
    n_neurons = 200
    n_outputs = 4
    n_layers = 2
    
    return n_steps, n_inputs, n_neurons, n_outputs, n_layers


def get_model():
    
    # model parameters
    n_steps, n_inputs, n_neurons, n_outputs, n_layers = get_model_config()
    
    # Define the RNN model
    class RNNModel(nn.Module):
        def __init__(self, n_inputs, n_neurons, n_layers, n_outputs):
            super(RNNModel, self).__init__()
            self.rnn = nn.RNN(input_size=n_inputs, hidden_size=n_neurons, num_layers=n_layers, nonlinearity='relu')
            self.fc = nn.Linear(n_neurons, n_outputs)

        def forward(self, x):
            rnn_outputs, _ = self.rnn(x)
            stacked_rnn_outputs = rnn_outputs.view(-1, self.rnn.hidden_size)
            stacked_outputs = self.fc(stacked_rnn_outputs)
            outputs = stacked_outputs.view(-1, n_steps, n_outputs)[:, -1, :]  # Keep only the last output
            return outputs
        
    model = RNNModel(n_inputs, n_neurons, n_layers, n_outputs)
    
    return model
    
    
def get_loss_function():
    criterion = nn.MSELoss()
    return criterion

def get_optimizer(model, lr):
    optimizer = optim.Adam(model.parameters(), lr)
    return optimizer    
    
def convert_to_tensor(x_train, y_train):
    X_train = torch.Tensor(x_train)
    y_train = torch.Tensor(y_train)
    return X_train, y_train

# ------------------------------------------------------------------

# (5) Trainig

def get_train_config():
    
    learning_rate = 0.001
    batch_size = 50
    n_epochs = 100
    
    return learning_rate, batch_size, n_epochs


def train():
    
    learning_rate, batch_size, n_epochs = get_train_config()
    
    model = get_model()
    criterion = get_loss_function()
    optimizer = get_optimizer(model, lr=learning_rate)
    
    x_train, y_train, x_valid, y_valid, x_test, y_test = split_data() # 수정 필요
    X_train, y_train = convert_to_tensor(x_train, y_train)

    
    # training loop
    for epoch in range(n_epochs):
        for iteration in range(0, train_set_size, batch_size):
            x_batch = X_train[iteration:iteration + batch_size]
            y_batch = y_train[iteration:iteration + batch_size]

            optimizer.zero_grad()  # Zero the gradients
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()  # Compute gradients
            optimizer.step()  # Update weights

        # Calculate and print the training and validation loss
        mse_train = criterion(model(X_train), y_train)
        mse_valid = criterion(model(torch.Tensor(x_valid)), torch.Tensor(y_valid))
        print(f"Epoch {epoch + 1}: MSE train/valid = {mse_train.item():.6f}/{mse_valid.item():.6f}")

