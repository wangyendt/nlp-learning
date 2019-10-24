# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wang121ye
# datetime: 2019/10/20 20:31
# software: PyCharm

import os
import shutil,re
import jieba
import matplotlib.pyplot as plt
import pandas as pd
from ndtpy.tools import list_all_files
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud, ImageColorGenerator

if __name__ == '__main__':
    result_root = 'result'
    # if os.path.exists(result_root):
    #     shutil.rmtree(result_root)
    # os.mkdir(result_root)
    document = []
    for file in list_all_files('data', ['', 'xlsx']):
        data = pd.read_excel(file)
        score = data['score']
        comment = data['content']
        df = data[['content', 'score']]
        df = df.loc[[any([keyword in comm for keyword in [
            '按键', '按压', '隐藏', '操控', '压力', '音量', '压感', '压力感应',
            '边框', '虚拟', '调节', '边缘', '触', '实体', '物理'
        ]]) for comm in comment]]
        for d in df['content']:
            document.append(d)

        df['sentiment'] = df['content'].map(lambda x: SnowNLP(x).sentiments)
        df.loc[df['sentiment'] < 0.5, '评价'] = '差评'
        df.loc[df['score'] == 5, '评价'] = '好评'
        df.loc[df['sentiment'] >= 0.5, '评价'] = '好评'
        num_good = sum(df['评价'] == '好评')
        num_all = len(df)
        print(file, num_good / num_all)
        df.to_excel(os.path.join(result_root, re.findall(
            r'\\([\da-z-_]*?)\.xlsx$', file
        )[0] + f'_好评率([{num_good}][{num_all}])result.xlsx'))
    word_split_jieba = jieba.cut('\n'.join(document), cut_all=False)
    word_space = ' '.join(word_split_jieba)
    img = imread('cat.jpg')
    with open('stop words.txt','r',encoding='utf-8') as f:
        stop_words = set([word.strip('\n') for word in f.readlines()])
    word_cloud = WordCloud(
        background_color='white',
        mask=img,
        max_words=200,
        stopwords=stop_words,
        font_path='simkai.ttf',
        max_font_size=100,
        min_font_size=10
    ).generate(word_space)
    image_color = ImageColorGenerator(img)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
    word_cloud.to_file(os.path.join(result_root, 'word_cloud.jpg'))
