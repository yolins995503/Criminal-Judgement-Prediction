#---------------------------------------------------------------------------------------------------------------------------
import os
import re
#斷詞
from ckiptagger import data_utils, construct_dictionary, WS
#word2vec
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
#-----------------------------------------------------------------------------------------------------------------------------
# 存停用詞的list
stopWords=[]
# 讀入停用詞檔
with open('stop_words.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)
#-----------------------------------------------------------------------------------------------------------------------------
#Use to remove punctuation
def remove_punctuation(line, strip_all=True):
  if strip_all:
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
  else:
    punctuation = """，。！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
    re_punctuation = "[{}]+".format(punctuation)
    line = re.sub(re_punctuation, "", line)
  return line.strip()
#---------------------------------------------------------------------------------------------------------------------------
#讀取訓練資料
Path = r'D:\pysource\project\trainset'
DataPath = []
for root, dirs, files in os.walk(Path): 
    for file in files:
        DataPath.append (root + r"\\" + file)
#--------------------------------------------------------------------------------------------------------------------------- 
# Load model
ws = WS(r'D:\pysource\ckiptagger\data')
#---------------------------------------------------------------------------------------------------------------------------
#執行斷詞
print ('斷詞開始')   
for i in range(len(DataPath)):
  sentence_list = []
  with open (DataPath[i],'r',encoding='UTF-8') as text:
    line = text.read()
    line = line.replace(u'\u3000','')
    line = line.replace(u' ','')
    line = line.replace(u'\n','')
    line = remove_punctuation(line)
    sentence_list.append(line)
    word_sentence_list = ws(sentence_list)
    wf = 'all_data_seg.txt'
    with open(wf, 'a',encoding="UTF-8") as output:
      for j in range(len(word_sentence_list)):
        word_sentence_list[j] = list(filter(lambda a: a not in stopWords and a != '\n',word_sentence_list[j])) #去除停用詞
        word_sentence_list[j]=str(word_sentence_list[j]).replace(u',',' ')
        word_sentence_list[j]=word_sentence_list[j].replace(u'\'','')
        word_sentence_list[j]=word_sentence_list[j].replace(u'[','')
        word_sentence_list[j]=word_sentence_list[j].replace(u']','')
        output.write(word_sentence_list[j])
        output.write("\n")
    output.close()
  text.close()
  if (i%5==0):
    print (i,"finish")
print ('斷詞結束')
#---------------------------------------------------------------------------------------------------------------------------
# Release model
del ws
#---------------------------------------------------------------------------------------------------------------------------
#word2vec
print ('word2vec開始')
sentence = LineSentence("all_data_seg.txt")
model = word2vec.Word2Vec(sentence, size=250)
model.save("word2vec.model")
print ('word2vec結束')
#---------------------------------------------------------------------------------------------------------------------------