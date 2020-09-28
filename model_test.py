#%%---------------------------------------------------------------------------------------------------------------
#import packages
import os
import re
import csv
import keras
import time
import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#word2vec
from gensim.models import Word2Vec
from gensim import models

#斷詞
import jieba

# tensorflow-keras
from keras.models import Sequential
from keras.layers import Dense, GRU, Embedding, LSTM, Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import RMSprop
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras.models import load_model

#進行訓練和測試樣本的分割
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

#%%---------------------------------------------------------------------------------------------------------------
#讀入word2vec model
word2vec_model = models.Word2Vec.load('word2vec_combine.model')
print('Found %s word vectors of word2vec' % len(word2vec_model.wv.vocab))


model = load_model('LSTM_class_1_傷害.model')

max_tokens = 980



#%%---------------------------------------------------------------------------------------------------------------
#讀入test_Data
test_data = pd.read_csv(r'test_data_1_傷害.csv',encoding='utf-8')

cols = ['主文','事實及理由','label']
test_data = test_data.loc[:, cols]
test_data['事實及理由'] = pd.DataFrame(test_data['事實及理由'].astype(str))

test_data.head(10)
#%%---------------------------------------------------------------------------------------------------------------
train_texts_orig = [] #用來儲存所有事實
for i in test_data['事實及理由'] :
    train_texts_orig.append(i)
#%%---------------------------------------------------------------------------------------------------------------
record = 0
def predict_sentiment(text):
    global record
    #print('===============================================================================================')
    #print("第",count,"篇",test_data['主文'][count])
    print("第",count,"篇")
    #print('===============================================================================================')
    #print(text)
    # 去标点
    text = re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",text)
    # 分词
    cut = jieba.cut(text)
    cut_list = [ i for i in cut ]
    # tokenize
    for i, word in enumerate(cut_list):
        try:
            cut_list[i] = word2vec_model.wv.vocab[word].index
        except KeyError:
            cut_list[i] = 0
    # padding
    tokens_pad = pad_sequences([cut_list], maxlen=max_tokens,padding='pre', truncating='pre')
    # 预测
    result = model.predict(x=tokens_pad)
    coef = result[0][0]
    if coef <= 0.5:
        flag = 1
        print('此例可能為勝訴','output=%.2f'%(1-coef))
    else:
        flag = 0
        print('此例可能為敗訴','output=%.2f'%(1-coef)) 
    if flag != test_data['label'][count] :
        record+=1
    print('主文結果', test_data['label'][count])
    print('目前篇數', count)
    print('累積錯誤篇數' ,record)
    print('===============================================================================================')

#%%---------------------------------------------------------------------------------------------------------------
# 分詞和tokenize
seconds = time.time()
# 將秒數轉為本地時間
local_time = time.ctime(seconds)
# 輸出結果
print("本地時間：", local_time)

count = 0
for text in train_texts_orig:
    predict_sentiment(text)
    count+=1

seconds = time.time()
# 將秒數轉為本地時間
local_time = time.ctime(seconds)
# 輸出結果
print("本地時間：", local_time)