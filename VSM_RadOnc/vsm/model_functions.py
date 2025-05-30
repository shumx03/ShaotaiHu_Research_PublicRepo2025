"""
W2V Model & Weight Functions
Created on Friday May 16 14:06:32 2025
@authors: Samuel luk, Shaotai Hu
"""

import os
import random
import re
import math
import pandas as pd
import numpy as np
import gensim
from gensim.models import Word2Vec
from sim_functions_final import cos_sim, eud_dis, man_dis
from vsm_functions_final import shuffle, build_corpus, tokenize, w2v_train, bal_ran_subsamp, total_words, vector_append, vector_gen, skl_tfidf

###__________ weights setup __________ ###

# Takes tokenized corpus
def count_term(data, node, term):
    count = 0
    for t in data[node]:
        if t == term:
            count+=1
    return count

# will be 3 layer dictionary
# aggregated cs_sim for a single subject in column
def aggregate_loc(data, nodes_in):
    N = len(data)
    temp_dict = {}
    temp_dict["total_per_node"] = N
    for node in nodes_in[1:len(nodes_in)]:
        #print(node)
        data[node] = data[node].astype(str)
        weights = {}
        # keep in mind every node is divide by N, not all nodes sum
        for e in data[node].unique():
            e_count = count_term(data, node, e)
            weights[e] = e_count
        temp_dict[node] = weights
        #print(f"Total Count: {N} \n")
        #print(f"{node}: {weights} \n")
    return temp_dict

###__________ model training __________ ###
def w2v_gen(data1_f, subject_locs, nodes_in):
    df_all = pd.DataFrame()
    final_weights_dict = {}

    for subject in subject_locs:

        data1 = data1_f[data1_f["column"] == subject_loc] 

        # used in weight calculation
        all_lower = data1.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        all_lower["subject1"] = "###_" + all_lower["subject1"].astype(str)
        #...

        toks1 = tokenize(build_corpus(data1, nodes_in))

        w2v_mall = Word2Vec(workers = 1, seed = 12345, min_count = 1000, vector_size = 1000)
        w2v_corall = w2v_train(w2v_mall, toks1) 

        cbw_results = {}
        for i in w2v_corall.wv.index_to_key:
            cbw_results[i] = []
        
        # hyperparameters are randomized for confidentiality
        for i in range(10):
            w2v_m1 = Word2Vec(workers = 1000,
                        seed = 12345,
                        vector_size = 1000,
                        window = 1000,
                        min_count = 1000,
                        epochs = 1000,
                        sg = 0,
                        cbow_mean = 1)

            w2v_cor1 = w2v_train(w2v_m1, shuffle(toks1)) 

            # stores the iterations of cos_sim models
            for i in w2v_corall.wv.index_to_key:
                cbw_results[i].append(w2v_cor1.wv[i])  

        ###__________ calculate weights __________ ###
        mean_results = {key: np.mean(value) for key, value in cbw_results.items()}

        layer2dict = aggregate_loc(all_lower, nodes_in)
        final_weights_dict[subject_loc] = layer2dict

        ###__________ __________ __________ ###

        # rename the subject loc column to cbw_loc to represent the single w2v value            
        cbw_results["cbw_loc"] = cbw_results.pop(subject_loc.lower())

        # turns into df and adds the subject loc in every row
        cbwdf = pd.DataFrame(cbw_results)
        cbwdf.insert(0, "subject_loc", f"{subject_loc}")

        # appends to overall df
        df_all = pd.concat([df_all, cbwdf], ignore_index = True)

        # moves the index of cbw_loc to 1
        cols = df_all.columns.tolist()
        cols.insert(1, cols.pop(cols.index("cbw_loc")))
        df_final = df_all[cols]

    return df_final, final_weights_dict

















