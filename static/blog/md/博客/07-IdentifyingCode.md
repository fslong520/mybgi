---
title: 07-使用Python的Pillow模块生成验证码
toc: true
date: 2018-04-13 14:04:35
categories: study
tags: [identifyingCode,Python,Pillow]
---
&emsp;&emsp;到了重头戏了，这一篇文章讲的是如何去生成验证码，后续会讲到如何识别验证码。我们用到一个第三方模块：Pillow，如果没有安装，可以在终端当中输入：`pip install pillow`注意，这里是**小写**的`pillow`。
&emsp;&emsp;先上效果图： 
![](https://wx2.sinaimg.cn/mw690/3c1b9c69ly1fqaw4cq88oj20v90iidq4.jpg)
&emsp;&emsp;是不是有种似曾相识的感觉，很多网站的验证码都是如此这般简洁（loù），主体思路如下：
1. 创建一个大的Image，用来当作整个验证码的背景，并且用随机的像素点填充；
2. 创建四个小的Image，每个小的Image上面写一个字符（因为要随机的角度旋转图片才能得到角度随机的字符，所以需要四个Image）；
3. 生成四个随机字符，并分别绘制在上一步创建的四个Image上；
4. 将四个绘制完随机字符的小Image分别随机旋转一个角度，**注意：角度不能过大，因为Z和N旋转90°是一样的；**
5. 将四个小Image粘贴到第一个Image上面，按照一定的错位关系排列，这里需要拆分通道，才能把四个小Image的透明背景粘贴到大的Image上，不然背景会被覆盖成创建小Image时设置的颜色，前面随机填充的背景像素点就会没有效果;
6. 将图片模糊处理。
&emsp;&emsp;代码如下：
```Python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 首先引入PIL模块，ImageFilter用于模糊图像，ImageDraw用于绘制图像，用于绘制字符
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
print('-------------------------------\n生成验证码测试\n-------------------------------\n')
'''
生成验证码
'''
def rndChar():
    # 随机一个计数器
    a = random.randint(1, 3)
    # 如果a==1返回大写字母
    if a == 1:
        return chr(random.randint(65, 90))
    # 如果a==2返回小写字母
    elif a == 2:
        return chr(random.randint(97, 122))
    # 如果a==3返回数字
    else:
        return chr(random.randint(48, 57))
def rndColor():
    # 返回随机颜色1，也就是背景颜色
    return (random.randint(64, 255), random.randint(64, 255),
            random.randint(64, 255))
def rndColor2():
    # 返回随机颜色2，也就是验证码的颜色
    return (random.randint(37, 127), random.randint(37, 127),
            random.randint(37, 127))
def identifyingCode():
    # 设置长是宽的4倍，也就是容纳4个字符
    width, height = 170 * 4, 170
    # 创建白色图片画板
    image = Image.new('RGBA', (width, height), (255, 255, 255))
    # 创建Draw对象，也就是画笔
    draw = ImageDraw.Draw(image)
    # 随机创建字体大小，这里有个坑，字体文件要么用绝对路径要么用小写的文件名
    font = []
    for i in range(4):
        font.append(ImageFont.truetype('arial.ttf', random.randint(30, 80)))
    # 用随机颜色填充画布的每个像素点
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 用随机字符、字体大小、随机颜色2填充四个字符的位置
    # 还要保存生成的字符串，用于以后查看是否匹配
    checkChar=[]
    for t in range(4):
        checkChar.append(rndChar())# 存储生成的验证码
        c = Image.new('RGBA', (170, 170))# 新建承载单个验证码字符的画布
        b = ImageDraw.Draw(c)# 新建单个验证码的画笔
    # 将验证码画到画布上
        b.text(
            (55 + random.randint(-10, 10), 55 + random.randint(-10, 10)),
            checkChar[t],
            font=font[t],
            fill=rndColor2())
    # 随机旋转验证码字符，必须是图片才能旋转
        c = c.rotate(random.randint(-45, 45))
    # 将验证码的各个单个字符粘贴到画布上，分理处各个颜色通道，并将透明图层作为mask的属性粘贴到image上，否则验证码字符的画布会变成白色粘贴进去，从而覆盖掉我们之前生成的背景颜色
        r, g, b, a = c.split()
    # 注意，粘贴的时候，第一个参数时你要粘贴的对象，第二个tuple是位置参数，如果只设置前两个参数表示的是左上角的位置，如果设置四个参数那就是左上角跟右下角坐标，此时必须的把参数算精确，除非大小能完全匹配，不然会报错，mask属性代表的是透明通道是否也粘贴进去，如果不设置，透明通道会被粘贴成白色。
        image.paste(c, (170 * t, 0), mask=a)
    # 模糊处理
    image = image.filter(ImageFilter.BLUR)
    # 保存验证码
    image.save('验证码.png', 'png')
    print('生成的验证码是：',checkChar)
    for i in range(4):
        checkChar[i]=checkChar[i].lower()    
    # 显示图片
    image.show()
    return checkChar
a=identifyingCode()
b=input('请输入看到的验证码:')
c=''
for i in a:
    c+=i
assert b==c
print('-------------------------------\n输入验证码正确，测试通过\n-------------------------------\n')
```
&emsp;&emsp;还是跟以往一样，注释很详细了，如有疑问可以给我发邮件或者微博留言（还没搞懂怎么在博客下面留言，诸位先将就吧），下一步我计划等时机合适了再写一下如何识别验证码。