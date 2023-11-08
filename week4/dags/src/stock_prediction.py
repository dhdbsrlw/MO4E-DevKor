from datetime import timedelta, datetime
import numpy as np
import pandas as pd
import sklearn
import sklearn.preprocessing
import matplotlib.pyplot as plt

### 데이터 넘기기 
### 서빙
### fastAPI
### 다음주부터 7시에 시작 

from pykrx import stock

# (1) setting part

# 인자값 수정 필요
def split_dataset(): 
    valid_set_size_percentage = 10
    test_set_size_percentage = 10

# (2) market data part

def get_today():
    dt_now = str(datetime.now().date())
    print(f'{dt_now} 기준')
    dt_now = ''.join(c for c in dt_now if c not in '-')
    return dt_now

# 오늘 날짜에 해당하는 주식 데이터 임포트
def get_market_fundamental():
    dt_now = get_today()
    df = stock.get_market_ohlcv("20230101", "{dt_now}", "005930") # 삼성 주가
    df.columns = ['open', 'high', 'low', 'close', 'volume', 'RoC'] # 영문으로 칼럼명 변경
    
    print(df.info())
    print(df.head())
    df.to_csv(f'./{dt_now}_market_fundamental.csv', index=True) 
    
def normalize_fundamental():
    dt_now = get_today()
    df = pd.read_csv(f'./{dt_now}_market_fundamental.csv', index_col=0)
   
    norm_df = df.copy()
    min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    norm_df['open'] = min_max_scaler.fit_transform(norm_df.open.values.reshape(-1,1))
    norm_df['high'] = min_max_scaler.fit_transform(norm_df.high.values.reshape(-1,1))
    norm_df['low'] = min_max_scaler.fit_transform(norm_df.low.values.reshape(-1,1))
    norm_df['close'] = min_max_scaler.fit_transform(norm_df['close'].values.reshape(-1,1))
    
    print(norm_df.head())
    norm_df.to_csv(f'./{dt_now}_norm_market_fundamental.csv', index=True)
  
def normalized_data_split():
    dt_now = get_today()
    norm_df = pd.read_csv(f'./{dt_now}_norm_market_fundamental.csv', index_col=0)
    seq_len = 20 # 임의 지정
    
    data_raw = norm_df.values
    data = []
    
    # create all possible sequences of length seq_len
    for index in range(len(data_raw) - seq_len):
        data.append(data_raw[index: index + seq_len])
        
    data = np.array(data);
    valid_set_size = int(np.round(valid_set_size_percentage/100*data.shape[0]));
    test_set_size = int(np.round(test_set_size_percentage/100*data.shape[0]));
    train_set_size = data.shape[0] - (valid_set_size + test_set_size);

    print(data)
    