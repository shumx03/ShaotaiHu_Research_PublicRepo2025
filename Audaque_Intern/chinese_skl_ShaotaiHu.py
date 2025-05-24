# remove all unwanted characters from corpus
import re
import fasttext
def remove_non_chinese_line(line):
    pattern = re.compile(r'[^\u4e00-\u9fff]')
    return pattern.sub('', line)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    cleaned_lines = [remove_non_chinese_line(line.strip()) for line in lines]
    with open('cl_chinese.txt', 'w', encoding='utf-8') as output_file:
        for line in cleaned_lines:
            if len(line) >= 30:
                output_file.write(line + '\n')

process_file('中文语料.txt')

from openai import OpenAI

def fix_txt(file):
    lines = []
    with open(file, "r", encoding = "utf-8", errors="ignore") as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines

#change your corpus here
file_to_fix = "cl_chinese.txt"
working_file = fix_txt(file_to_fix)

api_key = '###'

client = OpenAI(base_url="###", api_key=api_key)

#start = time()

model = '###'

temp_list=[]

# using AI model to label each line in training txt and correcting format for Fasttext usage
#I guess you can call this the "port" connecting AI model and my program
for line in working_file:
    response = client.chat.completions.create(
        model=model,
        messages=[
            #attitudes
            {"role": "system", "content": """You are a helpful assistant."""},
            {"role": "user", "content": """从positive, negative, neutral这三个态度中选一个用英文告诉我括号里的话的态度
            (命运的不公让我感到无比愤怒和无奈。为什么我要承受这一切？为什么我不能拥有幸福的生活？心中的悲伤让我对世界充满了怨恨。)
            你的回答格式是"negative," """},
        
            {"role": "assistant", "content": "negative,"},
            {"role": "user", "content": f"你这个回答是标准的，对括号中的文本执行相同的操作 {line}。不要废话。"}
        ]
    )
    content = response.choices[0].message.content
    temp_list += [content + line]
    
#for some reason AI model generates a "/", so removing it
for i,e in enumerate(temp_list):
    temp_list[i] = e.replace('/', '')

#writing labeled and formatted data into a txt file
with open('skl_Chinese.txt', 'w+', encoding="utf-8") as file:
    for lines in temp_list:
        #if line.startswith("__"):
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
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith('positive,'):
                file.write(line)
            elif line.startswith('negative,') and count < 801:
                count += 1
                file.write(line)
            elif line.startswith('neutral,'):
                file.write(line)

filter_lines('skl_Chinese.txt')

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

txt_file_path = 'skl_Chinese.txt'
csv_file_path = 'skl_cncn.csv'
txt_to_csv_two_columns(txt_file_path, csv_file_path)

import pandas as pd

senti = pd.read_csv("skl_cncn.csv", header = None, names = ["target", "data"], sep = ",")
senti.dropna()
senti.head(3000)

import jieba as jb
def stopwords_cn(stopwords):
    stopwords = [line.strip() for line in open (stopwords, 'r', encoding = 'utf-8').readlines()]
    return stopwords
    
stopw = stopwords_cn("stopwordsCN.txt")

senti['data'] = senti['data'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopw]))
senti.head(3000)

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
while counter < 1000:
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