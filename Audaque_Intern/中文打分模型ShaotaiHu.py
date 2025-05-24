# remove all unwanted characters from corpus
import re
import fasttext
def remove_non_chinese_line(line):
    pattern = re.compile(r'[^\u4e00-\u9fff]')
    #pattern = re.compile(r'[^a-zA-Z\s.,!?]')
    return pattern.sub('', line)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    cleaned_lines = [remove_non_chinese_line(line.strip()) for line in lines]
    with open('cleaned_lines.txt', 'w', encoding='utf-8') as output_file:
        for line in cleaned_lines:
            if len(line) >= 30:
                output_file.write(line + '\n')

process_file('中文语料.txt')

#from time import time 
from openai import OpenAI

def fix_txt(file):
    lines = []
    with open(file, "r", encoding = "utf-8", errors="ignore") as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines

#change your corpus here
file_to_fix = "cleaned_lines.txt"
working_file = fix_txt(file_to_fix)

####################################################################################################################################################
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
            你的回答格式是"__label__negative" """},
        
            {"role": "assistant", "content": "__label__negative"},
            {"role": "user", "content": f"你这个回答是标准的，对括号中的文本执行相同的操作 {line}。不要废话。"}
        ]
    )
    content = response.choices[0].message.content
    temp_list += [content + " " + line]
    
#for some reason AI model generates a "/", so removing it
for i,e in enumerate(temp_list):
    temp_list[i] = e.replace('/', '')

#writing labeled and formatted data into a txt file
with open('testCNcorpus.txt', 'w+', encoding="utf-8") as file:
    for lines in temp_list:
        #if line.startswith("__"):
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

filter_lines('testCNcorpus.txt')

neg_num = 0
pos_num = 0
neu_num = 0

last_txt = fix_txt("testCNcorpus.txt")
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
    with open('train_chinese.txt', 'w', encoding = "utf-8") as train_file:
        train_file.writelines(train_lines)
    with open('test_chinese.txt', 'w', encoding = "utf-8") as test_file:
        test_file.writelines(test_lines)

pre_list = []
i = 0
while i <= 49:
    i += 1
    split_file('testCNcorpus.txt')

    import fasttext

    #autoEN = fasttext.train_supervised(input="train_chinese.txt", autotuneValidationFile='test_chinese.txt', autotuneDuration = 10)
    model_chinese = fasttext.train_supervised(input="train_chinese.txt", lr = 0.9, epoch = 20, wordNgrams = 1, dim = 100, loss = "ova")

    result = model_chinese.test("test_chinese.txt")
    print("Precision" + " " + str(i) + ":" + str(result[1]))
    pre_list.append(result[1])

#from fasttext docs "precision is the number of correct labels among the labels predicted by fastText."
print("Top Precision: " + str(max(pre_list)))
print(model_chinese.labels)

# saving & loading the model

#model_chinese.save_model("model_chinese.bin")
#cnm = fasttext.load_model("model_chinese.bin")