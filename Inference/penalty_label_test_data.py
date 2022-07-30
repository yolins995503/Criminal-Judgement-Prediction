#---------------------------------------------------------------------------------------------------------------------------
import os
import re
import math
from operator import itemgetter 
import csv
import pandas as pd
#斷詞
from ckiptagger import data_utils, construct_dictionary, WS
#word2vec
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
from collections import Counter
from gensim import models
import logging
#-----------------------------------------------------------------------------------------------------------------
Path = r'D:\pysource\project\刑期label\新增資料夾'
DataPath = []
for root, dirs, files in os.walk(Path): 
    for file in files:
        DataPath.append (root + r"\\" + file)
row=0
count=0
record=[]
#合併
train = {
    "主文":[],
    "事實及理由" :[],
    "label" : [],
}
copy={
    "全文":[],
}
paraSeg_keywords = ["事實及理由","事實","犯罪事實及理由","犯罪事實","事實及證據","犯罪事實及證據","理由"]
paraSeg_keywords2 = ["主文"]
paraSeg_keywords3 = ["中華民國","證據"]
paraSeg_keywords4=["理由","事實及理由","犯罪事實及理由","事實及證據","犯罪事實及證據"]
record.append(row)
with open('all_data.txt','w',encoding='utf8') as output:
    for i in range(len(DataPath)):
        flag = 0
        flag2=5
        data = ['']*6
        with open (DataPath[i],'r',encoding='utf8') as text:
            for line in text:
                data[flag2]=data[flag2]+line
                line=line.replace(u'\u00A0','')
                line=line.replace(u'\u0020','')
                line=line.replace(u'\u3000','')
                line=line.replace(u'\n','')
                if(flag==0):
                    if line[0:2] in paraSeg_keywords2:
                        line = line+'\n'
                        flag=1
                if(flag==1 or flag==4):
                    if line[0:4] in paraSeg_keywords or line[0:5] in paraSeg_keywords or line[0:7] in paraSeg_keywords:
                        line = line+'\n'
                        flag=2
                if(flag==2):
                    if line[0:2] in paraSeg_keywords4 or line[0:4] in paraSeg_keywords4 or line[0:5] in paraSeg_keywords4 or line[0:7] in paraSeg_keywords4:
                        flag=4
                    if line[0:4] in paraSeg_keywords3 or line[0:2] in paraSeg_keywords3:
                        break
                line=line.replace(u' ','')
                line=line.replace(u'，','\n')
                line=line.replace(u'。','\n')
                line=line.replace(u'；','\n')
                data[flag]=data[flag]+line
            if len(data[2])<5000 and len(data[2])>0:
                copy['全文'].append(data[flag2])
                train['主文'].append(data[1])
                train['事實及理由'].append(data[2])
                output.write(data[1])
                count+=1
                for g in range(len(data[1])):
                    if data[1][g]=='\n':
                        row+=1
                output.write('\n\n')
                row+=2
                record.append(row)
        if(i%100 == 0):
            print('已處理文章數 : ' + str(i))
    print('文章合併完成')
    print(record)

# 存停用詞的list
stopWords=[]
# 讀入停用詞檔
with open('stop_words.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)

#Use to remove punctuation
def remove_punctuation(line, strip_all=True):
  if strip_all:
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
  else:
    punctuation = """ ！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
    re_punctuation = "[{}]+".format(punctuation)
    line = re.sub(re_punctuation, "", line)
  return line.strip()

#執行斷詞
# Load model
ws = WS(r'D:\pysource\ckiptagger\data')
#load file
fn = 'all_data.txt'
sentence_list = []
with open(fn, "r",encoding="utf-8") as Data:
    for line in Data:
        line= remove_punctuation(line)
        sentence_list.append(line)
# Run WS pipeline
    word_sentence_list = ws(sentence_list)
    # Release model
    del ws

#write the ws result into 'all_data_seg.txt'
wf = 'all_data_seg.txt'
with open(wf, 'w',encoding="utf-8") as output:
    for i in range(len(word_sentence_list)):
        word_sentence_list[i] = list(filter(lambda a: a not in stopWords and a != '\n',word_sentence_list[i])) #去除停用詞
        word_sentence_list[i]=str(word_sentence_list[i]).replace(u',',' ')
        word_sentence_list[i]=word_sentence_list[i].replace(u'\'','')
        word_sentence_list[i]=word_sentence_list[i].replace(u'[','')
        word_sentence_list[i]=word_sentence_list[i].replace(u']','')
        output.write(word_sentence_list[i])
        output.write("\n")
        if( i%1000 == 0):
            print('已處理斷詞行數 : ' + str(i))
    print('文章斷詞完成')

linecount=0
index=1
flag=0
with open('penalty.txt', 'w',encoding="utf-8") as mm:
    with open('all_data_seg.txt', 'r',encoding="utf-8") as output:
        for a in output.readlines():
            linecount+=1
            a=a.split( )
            if linecount == record[index]:
                flag=0
                index+=1
                mm.write('\n')
            with open('刑期.txt', 'r',encoding="utf-8") as money:
                for c in money.readlines():
                    if flag==0:
                        c=c.split( )
                        if list((filter(lambda g: g in c ,a))):
                            a=str(a).replace(u',',' ')
                            a=a.replace(u'\'','')
                            a=a.replace(u'[','')
                            a=a.replace(u']','')
                            a=a.replace(u'\u00A0','')
                            a=a.replace(u'\u0020','')
                            a=a.replace(u'\u3000','')
                            mm.write(str(a))
                            flag=1
                            break
                    '''
                    if flag==1:
                        c=c.split( )
                        if list((filter(lambda g: g in c ,a))):
                            a=str(a).replace(u',',' ')
                            a=a.replace(u'\'','')
                            a=a.replace(u'[','')
                            a=a.replace(u']','')
                            a=a.replace(u'\u00A0','')
                            a=a.replace(u'\u0020','')
                            a=a.replace(u'\u3000','')
                            mm.write("月")
                            flag=2
                            break
                    '''
#--------------------------------------------------------------------------------------------------------------------------------------
#中文大寫轉數字

def convert_cndigit(xxx):
    CN_NUM = {
        '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
        '壹' : 1, '貳' : 2, '參' : 3, '肆' : 4, '伍' : 5, '陸' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '兩' : 2,
    }

    CN_UNIT = {
        '十' : 10,
        '拾' : 10,
        '百' : 100,
        '佰' : 100,
        '千' : 1000,
        '仟' : 1000,
        '万' : 10000,
        '萬' : 10000,
        '亿' : 100000000,
        '億' : 100000000,
        '兆' : 1000000000000,
    }

    regex = re.compile(r'[零壹貳參肆伍陸柒捌玖貮兩十拾百佰千仟万萬亿億兆元角分年月日]+')
    xxx = regex.search(xxx)
    if xxx:
        xxx = xxx.group()
    else:
        return None
    result = 0
    result_list = []
    unit = 0
    control = 0
    for i, d in enumerate(xxx):
        if d in '零百佰千仟万萬亿億兆〇' and i == 0:
            return '大写数字格式有误'
            break
        if d == '元':
            continue
        if d == '日':
            continue
        if d == '角':
            result -= CN_NUM[xxx[i - 1]]
            result += CN_NUM[xxx[i - 1]] * 0.1
            continue
        if d == '年':
            result -= CN_NUM[xxx[i - 1]]
            result += CN_NUM[xxx[i - 1]] * 365
            continue
        if d == '月':
            result -= CN_NUM[xxx[i - 1]]
            result += CN_NUM[xxx[i - 1]] * 30
            continue
        if d in CN_NUM:
            result += CN_NUM[d]            
        elif d in CN_UNIT:
            if unit == 0:
                unit_1 = CN_UNIT[d]
                if result == 0:
                    result = CN_UNIT[d]
                else:
                    result *= CN_UNIT[d]
                unit = CN_UNIT[d]
                result_1 = result
            elif unit > CN_UNIT[d]:
                result -= CN_NUM[xxx[i - 1]]
                result += CN_NUM[xxx[i - 1]] * CN_UNIT[d]
                unit = CN_UNIT[d]
            elif unit <= CN_UNIT[d]:
                if (CN_UNIT[d] < unit_1) and (len(result_list) == control):
                    result_list.append(result_1)
                    result = (result - result_1) * CN_UNIT[d]
                    control += 1
                else:
                    result *= CN_UNIT[d]
                unit = CN_UNIT[d]
                if len(result_list) == control:
                    unit_1 = unit
                    result_1 = result
        else:
            return '出现了不能匹配的中文数字，请查验'
            break
    return sum(result_list) + result

cal = [0]*100001
with open('penaltyresult1.txt', 'w',encoding="utf-8") as ben:
    with open('penalty.txt', 'r',encoding="utf-8") as mm:
        for a in mm.readlines():
            try:
                result = convert_cndigit(a)
                if result=='大写数字格式有误' or  result=='出现了不能匹配的中文数字，请查验':
                    train['label'].append("error")
                elif result==None:
                    #print('0')
                    ben.write('0')
                    ben.write('\n')
                    train['label'].append('0')
                else:
                    #print(result)
                    try:
                        cal[int(result)]+=1
                    except:
                        cal[0]+=1
                    ben.write(str(result))
                    ben.write('\n')
                    if int(result)<=30 and int(result)>=0:
                        train['label'].append('0')
                    elif int(result)<=90 and int(result)>30:
                        train['label'].append('1')
                    elif int(result)<=150 and int(result)>90:
                        train['label'].append('2')
                    elif int(result)<=210 and int(result)>150:
                        train['label'].append('3')
                    elif int(result)<=270 and int(result)>210:
                        train['label'].append('4')
                    elif int(result)>270:
                        train['label'].append('5')        
            except:
                train['label'].append("error")
for u in range(100001):
    if cal[u]>0:
        print(u,cal[u])

q1=0
q2=0
q3=0
q4=0
q5=0
q6=0

for i in range(count):
    # 寫入資料
    try:
        if train['label'][i]!="error" and train['label'][i]=='0':
            with open(r'D:\pysource\project\刑期label\刑期分類\0-30'+r"\\"+"data"+str(q1)+".txt",mode="w",encoding="utf-8") as file1:
                file1.write(copy['全文'][i])
                q1+=1
        if train['label'][i]!="error" and train['label'][i]=='1':
            with open(r'D:\pysource\project\刑期label\刑期分類\31-90'+r"\\"+"data"+str(q2)+".txt",mode="w",encoding="utf-8") as file2:
                file2.write(copy['全文'][i])
                q2+=1
        if train['label'][i]!="error" and train['label'][i]=='2':
            with open(r'D:\pysource\project\刑期label\刑期分類\91-150'+r"\\"+"data"+str(q3)+".txt",mode="w",encoding="utf-8") as file3:
                file3.write(copy['全文'][i])
                q3+=1
        if train['label'][i]!="error" and train['label'][i]=='3':
            with open(r'D:\pysource\project\刑期label\刑期分類\151-210'+r"\\"+"data"+str(q4)+".txt",mode="w",encoding="utf-8") as file4:
                file4.write(copy['全文'][i])
                q4+=1
        if train['label'][i]!="error" and train['label'][i]=='4':
            with open(r'D:\pysource\project\刑期label\刑期分類\211-270'+r"\\"+"data"+str(q5)+".txt",mode="w",encoding="utf-8") as file5:
                file5.write(copy['全文'][i])
                q5+=1
        if train['label'][i]!="error" and train['label'][i]=='5':
            with open(r'C:\Users\user\Desktop\刑期label\刑期分類\271-'+r"\\"+"data"+str(q6)+".txt",mode="w",encoding="utf-8") as file6:
                file6.write(copy['全文'][i])
                q6+=1
    except Exception as e :
        print(i)
        print(e)

print(q1)
print(q2)
print(q3)
print(q4)
print(q5)
print(q6)







'''
c0=2455
c1=2260
c2=1845
c3=2703
c4=1641
c5=1532
#寫入csv
with open('penalty_predict_test_data0.csv','a',newline='',encoding='utf-8') as csvfile0:
    with open('penalty_predict_test_data1.csv','a',newline='',encoding='utf-8') as csvfile1:
        with open('penalty_predict_test_data2.csv','a',newline='',encoding='utf-8') as csvfile2:
            with open('penalty_predict_test_data3.csv','a',newline='',encoding='utf-8') as csvfile3:
                with open('penalty_predict_test_data4.csv','a',newline='',encoding='utf-8') as csvfile4:
                    with open('penalty_predict_test_data5.csv','a',newline='',encoding='utf-8') as csvfile5:
                        # 定義欄位
                        fieldnames = ['主文','事實及理由','label']
                        # 將 dictionary 寫入 CSV 檔
                        writer0 = csv.DictWriter(csvfile0, fieldnames=fieldnames)
                        writer1 = csv.DictWriter(csvfile1, fieldnames=fieldnames)
                        writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames)
                        writer3 = csv.DictWriter(csvfile3, fieldnames=fieldnames)
                        writer4 = csv.DictWriter(csvfile4, fieldnames=fieldnames)
                        writer5 = csv.DictWriter(csvfile5, fieldnames=fieldnames)
                        # 寫入第一列的欄位名稱
                        writer0.writeheader()
                        writer1.writeheader()
                        writer2.writeheader()
                        writer3.writeheader()
                        writer4.writeheader()
                        writer5.writeheader()
                        for i in range(count):
                            # 寫入資料
                            try:
                                if train['label'][i]!="error" and train['label'][i]=='0':
                                    writer0.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
                                    c0+=1
                                if train['label'][i]!="error" and train['label'][i]=='1':
                                    writer1.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
                                    c1+=1
                                if train['label'][i]!="error" and train['label'][i]=='2':
                                    writer2.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
                                    c2+=1
                                if train['label'][i]!="error" and train['label'][i]=='3':
                                    writer3.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
                                    c3+=1
                                if train['label'][i]!="error" and train['label'][i]=='4':
                                    writer4.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
                                    c4+=1
                                if train['label'][i]!="error" and train['label'][i]=='5':
                                    writer5.writerow({'主文':train['主文'][i], '事實及理由':train['事實及理由'][i], 'label':train['label'][i]})
                                    c5+=1
                            except Exception as e :
                                print(i)
                                print(e)
print(c0)
print(c1)
print(c2)
print(c3)
print(c4)
print(c5)
'''