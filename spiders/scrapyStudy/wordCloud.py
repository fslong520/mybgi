#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 词云玩玩 '

__author__ = 'fslong'
import json
import os
import pickle

import jieba
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, ImageColorGenerator, WordCloud

path = os.path.dirname(__file__)
with open(os.path.join(path, 'win4000.json'), 'r', encoding='utf-8') as f:
    a = json.load(f)
    wordStr = ''
    for i in a:
        #print(i)
        wordStr += i['picName']
    print(wordStr)
wordStr=wordStr.replace('手机','')
wordStr=wordStr.replace('壁纸','')
text = ''
# 分词
text += ' '.join(jieba.cut(wordStr))
backgroud_Image = plt.imread(os.path.join(path, 'test.jpg'))
print('加载图片成功！')
'''设置词云样式'''
wc = WordCloud(
    background_color='white',  # 设置背景颜色
    mask=backgroud_Image,  # 设置背景图片
    font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
    max_words=2000,  # 设置最大现实的字数
    stopwords=STOPWORDS,  # 设置停用词
    max_font_size=80,  # 设置字体最大值
    random_state=100  # 设置有多少种随机生成状态，即有多少种配色方案
)
# 加载文本
wc.generate_from_text(text)
print('开始加载文本')
# 改变字体颜色
img_colors = ImageColorGenerator(backgroud_Image)
# 字体颜色为背景图片的颜色
wc.recolor(color_func=img_colors)
# 显示词云图
plt.imshow(wc)
# 是否显示x轴、y轴下标
plt.axis('off')
plt.show()
# os.path.join()：  将多个路径组合后返回
wc.to_file(os.path.join(path, 'test1111.jpg'))
print('生成词云成功!')
