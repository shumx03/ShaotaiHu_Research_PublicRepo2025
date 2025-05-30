"""
VSM Functions
Created on Monday Feb 10 20:10:35 2025
@authors: Samuel luk, Shaotai Hu
"""

### Packages ###
import pandas as pd
import numpy as np
import math
from numpy import dot
from numpy.linalg import norm
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
from gensim.models import Word2Vec
import random

### Preprocessing ###
def shuffle(corpus):
    #redacted
    return copy

def build_corpus(df, nodes_in):
    corpus = []
    nodes = df[nodes_in]
    for _, i in nodes.iterrows():
        doc = f"{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]}" 
        corpus.append(doc)
    return corpus

def tokenize(corpus):
    pattern = r'\S+'
    tokenized_corpus = [re.findall(pattern, sentence.lower()) for sentence in corpus]
    return tokenized_corpus

def w2v_train(model, corpus):
    model.build_vocab(corpus)
    model.train(corpus, total_examples = model.corpus_count, epochs = model.epochs)
    return model

# To sample equal num of sentences for each subject location in the entire data
def bal_ran_subsamp(data, num):
    temp_df = []
    for loc in subject_locs:
        loc_df = data[data["column"]==loc]
        ran_samp = loc_df.sample(n=num, random_state = 42, replace = False)
        temp_df.append(ran_samp)
    balanced_df = pd.concat(temp_df)
    return balanced_df

# Takes tokenized corpus
def total_words(corpus):
    return sum(len(sentence) for sentence in corpus)

### TF ###
#....
    
### sklearn TF_IDF ###
def skl_tfidf(corpora, corpus1):
    # words that appear in 95%+ documents are removed
    vectorizer = TfidfVectorizer(token_pattern = r'\S+', max_df=0.95, smooth_idf = False)
    idf_corpora = vectorizer.fit_transform(corpora)
    
    tfidf_matrix1 = idf_corpora[:len(corpus1)].toarray()
    tfidf_matrix2 = idf_corpora[len(corpus1):].toarray()

    skl1_vec = np.mean(tfidf_matrix1, axis = 0)
    skl2_vec = np.mean(tfidf_matrix2, axis = 0)

    return skl1_vec, skl2_vec
