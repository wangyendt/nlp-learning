# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wang121ye
# datetime: 2019/10/20 20:31
# software: PyCharm

import os
import re
import shutil

import pandas as pd
from ndtpy.tools import list_all_files
from snownlp import SnowNLP

if __name__ == '__main__':
    result_root = 'result'
    if os.path.exists(result_root):
        shutil.rmtree(result_root)
    os.mkdir(result_root)
    for file in list_all_files('practice', ['data', 'xlsx']):
        data = pd.read_excel(file)
        score = data['score']
        comment = data['content']
        df = data[['content', 'score']]
        df = df.loc[[any([keyword in comm for keyword in [
            '按键', '按压', '隐藏', '操控', '压力', '音量', '压感', '压力感应',
            '边框', '虚拟', '调节', '边缘', '触', '实体', '物理'
        ]]) for comm in comment]]

        df['sentiment'] = df['content'].map(lambda x: SnowNLP(x).sentiments)
        df.loc[df['sentiment'] < 0.5, '评价'] = '差评'
        df.loc[df['score'] == 5, '评价'] = '好评'
        df.loc[df['sentiment'] >= 0.5, '评价'] = '好评'
        num_good = sum(df['评价'] == '好评')
        num_all = len(df)
        print(file, num_good/num_all)
        df.to_excel(os.path.join(result_root, re.findall(
            r'\\([\da-z-_]*?)\.xlsx$', file
        )[0] + f'_好评率([{num_good}][{num_all}])result.xlsx'))
