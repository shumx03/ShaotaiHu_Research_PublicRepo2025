# remove all unwanted characters from corpus
import re

def remove_non_english(line):
    #pattern = re.compile(r'[^\u4e00-\u9fff，。！？、：；“”‘’]')
    pattern = re.compile(r'[^a-zA-Z\s]')
    return pattern.sub('', line)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    cleaned_lines = [remove_non_english(line.strip()) for line in lines]
    with open('cleaned_EN.txt', 'w', encoding='utf-8') as output_file:
        for line in cleaned_lines:
            if len(line) >= 30:
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
file_to_fix = "cleaned_EN.txt"
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
            {"role": "user", "content": """attitudes are either positive, negative , neutral, 
            output the attitude of the following text in brackets 
            (I ate very good food for lunch, and I am very happy right now.)
            answer in the format of "__label__attitude" """},
        
            {"role": "assistant", "content": "__label__positive"},
            {"role": "user", "content": f"This is a good answer, do the same for the text in brackets {line}"}

        ]
    )
    content = response.choices[0].message.content
    train_list += [content + " " + line]
    
#for some reason AI model generates a "/", so removing it
for i,e in enumerate(train_list):
    train_list[i] = e.replace('/', '')

#writing labeled and formatted data into a txt file
with open('labeled_EN.txt', 'w') as file:
    for lines in train_list:
        file.write('%s\n' %lines)
    
#end = time()
#time_used = end - start
#speed = len(content) / time_used
#print(f'speed: {speed:.4f} char/s')

def filter_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith('__label__positive '):
                file.write(line)
            elif line.startswith('__label__negative '):
                file.write(line)
            elif line.startswith('__label__neutral '):
                file.write(line)

filter_lines('labeled_EN.txt')

neg_num = 0
pos_num = 0
neu_num = 0

last_txt = fix_txt("labeled_EN.txt")
for gg in last_txt:
    if gg.startswith('__label__positive '):
        pos_num += 1
    elif gg.startswith('__label__negative '):
        neg_num += 1
    elif gg.startswith('__label__neutral '):
        neu_num += 1

print("negative percent: " + str(neg_num/len(last_txt)))
print("positive percent: " + str(pos_num/len(last_txt)))
print("neutral percent: " + str(neu_num/len(last_txt)))

import random
def split_file(file_path, train_ratio=0.9):
    with open(file_path, 'r', encoding = "utf-8") as file:
        lines = file.readlines()
    random.shuffle(lines)
    train_size = int(len(lines) * train_ratio)
    train_lines = lines[:train_size]
    test_lines = lines[train_size:]
    # Save the training and testing datasets to separate files
    with open('trainEN_corpus.txt', 'w', encoding = "utf-8") as train_file:
        train_file.writelines(train_lines)
    with open('testEN_corpus.txt', 'w', encoding = "utf-8") as test_file:
        test_file.writelines(test_lines)

pre_list = []
i = 0
while i <= 49:
    i += 1
    split_file('labeled_EN.txt')

    # single model testing
    import fasttext

    #autoEN = fasttext.train_supervised(input="trainEN_corpus.txt", autotuneValidationFile='testEN_corpus.txt', autotuneDuration = 10)
    modelEN = fasttext.train_supervised(input="trainEN_corpus.txt", lr = 0.9, epoch = 20, wordNgrams = 1, dim = 100, loss = "ova")

    result = modelEN.test("testEN_corpus.txt")
    print("Precision" + " " + str(i) + ":" + str(result[1]))
    pre_list.append(result[1])

#print(modelEN.labels)

#from fasttext docs "precision is the number of correct labels among the labels predicted by fastText."
print("Top Precision: " + str(max(pre_list)))