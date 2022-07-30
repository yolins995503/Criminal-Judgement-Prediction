#-------------------------------------------------------------------------------------------------------------------------------
import os
import re
import csv
import pandas as pd
#斷詞
from ckiptagger import data_utils, construct_dictionary, WS
# Load model
# ws = WS(r'E:\python\ckiptagger-master\data')
#-------------------------------------------------------------------------------------------------------------------------------
#讀取訓練資料
Path = r'D:\pysource\project\種類分類\裁判分類\訓練資料\毒品'
DataPath = []   
for root, dirs, files in os.walk(Path): 
    for file in files:
        DataPath.append (root + r"\\" + file)
#-------------------------------------------------------------------------------------------------------------------------------
#判決書分段
train = {
    "DataName":[],
    "主文":[],
    "事實及理由" :[],
    "label" : []
}
paraSeg_keywords = ["主文","事實","犯罪事實"]
paraSeg_keywords2 = ["中華民國","理由","事實及理由","犯罪事實及理由"]
count = 0
for i in range(len(DataPath)):
    #if count <50:
        flag = 0
        Data = ['']*4
        with open (DataPath[i],'r',encoding='utf8') as text:
            for line in text:
                line=line.replace(u'\u00A0','')
                line=line.replace(u'\u0020','')
                line=line.replace(u'\u3000','')
                line=line.replace(u'\ue972','')
                line=line.replace(u'\n','')
                if(flag<2):
                    if line[0:4] in paraSeg_keywords or line[0:5] in paraSeg_keywords or line[0:7] in paraSeg_keywords:
                        flag+=1
                        line = line+'\n'
                if(flag==2):
                    if line[0:4] in paraSeg_keywords2:
                        flag = 3
                line=line.replace(u' ','')
                line=line.replace(u'，','\n')
                line=line.replace(u'。','\n')
                Data[flag] = Data[flag]+line
            Data[flag] = Data[flag] + '\n'
            if (len(Data[2])>0):
                train['DataName'].append(files[i])
                train['主文'].append(Data[1])
                train['事實及理由'].append(Data[2])
                train['label'].append('3')
                count+=1
        text.close()
        if(i % 100 == 0):
            print('已處理文章數 : ' + str(i))
print('文章分段完成')
#-------------------------------------------------------------------------------------------------------------------------------
'''
#判斷勝負
positive_word=["有期徒刑","拘役","罰金"]
rule = re.compile(u"[^a-zA-Z\u4e00-\u9fa5]")
count=0
for i in train['主文']:
    sentence_list =[]
    train['label'].append('0')

    j=rule.sub('',i)
    sentence_list.append(j)
    
    word_sentence_list = ws(sentence_list)
    for word in word_sentence_list:
        for word2 in word:
            if word2 in positive_word:
                train['label'][count]=1
    count+=1
    if(count % 100 == 0):
        print('已處理文章數 : ' + str(count))
print(count)
print('文章label完成')
'''
#del ws
#-------------------------------------------------------------------------------------------------------------------------------
#寫入csv
with open('train_data_4_1.csv','a',newline='',encoding='utf-8') as csvfile:
    # 定義欄位
    fieldnames = ['主文','事實及理由','label']
    # 將 dictionary 寫入 CSV 檔
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # 寫入第一列的欄位名稱
    #writer.writeheader()
    for i in range(count):
        # 寫入資料
        try:
            writer.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
        except Exception as e :
            print(i)
            print(e)
