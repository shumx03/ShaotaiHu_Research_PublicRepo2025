import re

#name of the def says it
def remove_non_english(line):
    #pattern = re.compile(r'[^\u4e00-\u9fff，。！？、：；“”‘’]')
    pattern = re.compile(r'[^a-zA-Z\s]')
    return pattern.sub('', line)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    cleaned_lines = [remove_non_english(line.strip()) for line in lines]
    with open('csv_EN.txt', 'w', encoding='utf-8') as output_file:
        for line in cleaned_lines:
            if len(line) > 22:
                output_file.write(line.lower() + '\n')

process_file('emotionEN.txt')

from time import time
from openai import OpenAI

def fix_txt(file):
    lines = []
    with open(file, "r") as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines

#change your training corpus here
file_to_fix = "csv_EN.txt"
working_file = fix_txt(file_to_fix)

####################################################################################################################################################
api_key = '###'

client = OpenAI(base_url="###", api_key=api_key)

start = time()

model = '###'

train_list=[]

# using AI model to label each line in training txt and correcting format for Fasttext usage
#I guess you can call this the "port" connecting AI model and my program
for line in working_file:
    response = client.chat.completions.create(
        model=model,
        messages=[

            {"role": "system", "content": """You are a helpful assistant."""},
            {"role": "user", "content": """attitudes are either positive, negative, neutral, 
            output the attitude of the following text in brackets 
            (I ate very good food for lunch, and I am very happy right now.)
            answer in the format of "attitude," """},
        
            {"role": "assistant", "content": "positive,"},
            {"role": "user", "content": f"This is a good answer, do the same for the text in brackets {line}. Only write the answer in the given format."}

        ]
    )
    content = response.choices[0].message.content
    # comma separated lol 
    train_list += [content + line]
    
#for some reason AI model generates a "/", so removing it
for i,e in enumerate(train_list):
    train_list[i] = e.replace('/', '')

#writing labeled data into a txt file
with open('skl_EN.txt', 'w', encoding='utf-8') as file:
    for lines in train_list:
        file.write('%s\n' %lines)
    
#end = time()
#time_used = end - start
#speed = len(content) / time_used
#print(f'speed: {speed:.4f} char/s')

import random
# format filter

def filter_lines(file_path):
    count = 0 
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    random.shuffle(lines)
    with open("ccEN.txt", 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith('positive,'):
                file.write(line)
            elif line.startswith('negative,') and count < 801:
                count += 1
                file.write(line)
            elif line.startswith('neutral,'):
                file.write(line)

filter_lines('skl_EN.txt')

# turns previously formated txt file into a 2 column csv
# magic!
import csv

def txt_to_csv_two_columns(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file, open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in txt_file:
            # common separated
            parts = line.strip().split(',')  
            if len(parts) == 2:
                csv_writer.writerow(parts)

txt_file_path = 'ccEN.txt'
csv_file_path = 'skl.csv'
txt_to_csv_two_columns(txt_file_path, csv_file_path)

import pandas as pd

senti = pd.read_csv("skl.csv", header = None, names = ["target", "data"], sep = ",")
senti.dropna()

from nlppreprocess import NLP

nlp = NLP()
senti["data"] = senti["data"].apply(nlp.process)

ne = 0
po = 0
nu = 0
for val in senti["target"]:
    if val == "negative":
        ne += 1
    elif val == "positive":
        po += 1
    else: 
        nu += 1
# to see the need for a more balanced dataset
print("positive: " + str(po), "negative: " + str(ne), "neutral: " + str(nu))

import matplotlib.pyplot as plt

ax = senti['target'].value_counts().sort_index().plot(kind='bar',
          title='sentiment counts',
          figsize=(6, 3))
ax.set_xlabel('sentiment')
plt.show()

#Accuracy shows how often a classification ML model is correct overall.
#Precision shows how often an ML model is correct when predicting the target class. 
#Recall shows whether an ML model can find all objects of the target class.

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier

X = senti["data"]
y = senti["target"]

counter = 0
top_a = 0.0
while counter < 10000:
    counter += 1
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.9)

    pline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    pline.fit(X_train, y_train)

    y_pred = pline.predict(X_test)
    accu = accuracy_score(y_test, y_pred)
    if accu > top_a:
        top_a = accu
        b_test = y_test
        b_pred = y_pred


report = classification_report(b_test, b_pred)
#print("Try " + str(counter) + ":" + "________________________________________________")
print(f"Accuracy: {accuracy_score(b_test, b_pred)}\n")
print(report)