import os
import re
#斷詞
from ckiptagger import data_utils, construct_dictionary, WS
#word2vec
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
model = word2vec.Word2Vec.load("word2vec_combine.model")
more_sentence = LineSentence("all_data_seg_賭博.txt")
model.build_vocab(more_sentence,update=True)
model.train(more_sentence,total_examples=model.corpus_count,epochs=model.iter)
model.save("word2vec_combine.model")