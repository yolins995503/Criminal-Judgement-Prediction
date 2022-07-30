# Criminal Judgement Prediction

![](https://i.imgur.com/8ZHBqAs.png)

## Crawler

To collect the criminal case

Url Base : https://law.judicial.gov.tw/FJUD/Default_AD.aspx

Add the criminal case type in line 101
```
# line 101
self.driver.find_element(By.ID, "jud_title").send_keys("criminal case type")
```


law_craw_stable.py is the more stable one
```
python crawler/law_craw_stable.py
```

## Preprocessing

To generate the training data and testing data

Split the 1.主文 2.事實及理由 from the judgement and generate CSV
Remember to add the hearder of CSV during the first time

```
# line 92 
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
```
**Start preporcessing**
```
python Preprocessing/markcsv.py
```

Select the imprisonment time data 

```
#line 282~293
```
**Start preporcessing**

```
python Preprocessing/penalty_label_test_data.py
```

##  Word Embedding

To train the word2vec model
Select the dimension in line 73
```
#line 73
model = word2vec.Word2Vec(sentence, size=250)
```
**Start embedding**
```
python Word Embedding/trainword2vec.py
```

**Combine Different of Word2vec**

```
python Word Embedding/combineword2vec.py
```
## Train
To train Bilstm using Ckiptagger

Select the word2vec model(.model) in line 47
```
#line 47
word2vec_model = models.Word2Vec.load('all_class.model')
```

Select the Training data in line 51
```
#line 51
data = pd.read_csv('class_classification_test_train.csv',encoding='utf-8')
```

Select the max token in line 142
```
#line 142
max_tokens = 980
```
Select the num_class in line 213
```
#line 213
model.add(Dense(6, activation='softmax'))
```


**Start train**
```
python Train/trainlstm_ckip.py
```


## Inference

Inference the Word2vec

Select the model in line 6
```
#line 6 
model = models.Word2Vec.load('word2vec.model')
```
**Start inference**
```
python Inference/trainoutword2vec.py
```

Infernece the Bilstm

Select the model in line 43
```
#line 43
model = load_model('LSTM_class_1_傷害.model')
```
Select the testing data in line 51
```
line 51
test_data = pd.read_csv(r'test_data_1_傷害.csv',encoding='utf-8')
```
**Start inference**
```
python Inference/model_test.py
```