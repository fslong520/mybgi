---
title: 05-通过解析XML获取Bing每日美图并保存到本地
toc: true
date: 2018-04-12 14:02:22
categories: study
tags: [Python,XML,Bing美图]
---
&emsp;&emsp;上一篇文章我们介绍了通过解析Json格式的数据来获取Bing每日美图并保存到本地，这篇文章是在我学习完解析使用Python解析XML之后编写的，讲道理解析XML真是件***的事情。  
&emsp;&emsp;当然还是先上代码：

    from urllib.request import urlopen, urlretrieve
    from xml.parsers.expat import ParserCreate
    import os, re, json
    with urlopen('https://cn.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=2') as page1:
        picUrl1 = page1.read().decode('utf-8')  # 其实个人认为一行一行得读取比较安全
    class GetBingPicByXml(object):
        def __init__(self):  # 因为需要返回解析得数据，所以必须有这一个
            self.picDict = {
                'images': [],
                'tooltips':{}
            }
            self.name = ''  # 定义一个name,用于在char_element中判断
            self.i=-1
            self.j=0
        def start_element(self, name, attrs):
            self.name = name
            if name=='image':
                self.i+=1
                self.picDict['images'].append({})
            elif name=='tooltips':
                self.j=1
        def char_element(self, text):
            if self.j ==0:
                self.picDict['images'][self.i][self.name]=text
            else:        
                self.picDict['tooltips'][self.name]=text
        def end_element(self, name):
            pass
    def bingPicXml(xml_str):
        handler = GetBingPicByXml()
        parser = ParserCreate()
        parser.StartElementHandler = handler.start_element
        parser.CharacterDataHandler = handler.char_element
        parser.EndElementHandler = handler.end_element
        parser.Parse(xml_str)
        return handler.picDict
    result = bingPicXml(picUrl1)
    resultJson=json.dumps(result,ensure_ascii=False)
    print(resultJson)
&emsp;&emsp;现在解析下上面的代码：
1. ``from urllib.request import urlopen, urlretrieve``、``from xml.parsers.expat import ParserCreate``与``import os, re``引入了我们需要使用urllib模块（用于访问网址，抓取网址数据），及用于解析数据的xml、os以及re模块；
2. ``with urlopen('https://cn.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=2') as page1:``是使用urlopen方法打开网址，上篇文章也讲过，这里format=xml标识的的是返回xml格式的数据；
3. ``picUrl1 = page1.read().decode('utf-8')``是读取到数据，然后再decode成utf-8编码的字符串；
4. ``class GetBingPicByXml(object):``这个类用于定义需要返回或是要用到的数据以及对数据怎样处理，比如本例中在``__init__(self)``函数中定义了返回数据用的字典：picDict；用于后续判断标签的字符串：name；两个计数器i和j；
5. ``start_element(self, name, attrs)``、``char_element(self, text)``、``end_element(self, name)``分别表示读取到标签开始时、标签内容、标签结尾是做的事（参数表必须这样写），这三个函数其实写的很简单，就是标签开始时给self.name赋值标签名用于在，然后在读取到标签名是images的话picDict列表长度加一，然后再在char_element里将内容添加到列表里；
6. 到了``bingPicXml(xml_str)``函数是开始解析，首先通过``handler = GetBingPicByXml()``新建一个类handler,然后通过``parser = ParserCreate()``创建一个parser，然后再进行函数的绑定``parser.StartElementHandler = handler.start_element``、``parser.CharacterDataHandler = handler.char_element``、``parser.EndElementHandler = handler.end_element``,再使用Parse()函数进行解析``parser.Parse(xml_str)``，最后返回handler.picDict；
7. 为方便使用，又将返回的dict格式化成了json，此时需要注意的是，默认是ASCII编码的数据，汉字会变成二进制返回，所以在使用dumps格式化成json的时候需要设置``ensure_ascii=False``。  
### 总结：
&emsp;&emsp;通过上述代码，最终又格式化成了json输出如图：![解析结果](https://wx2.sinaimg.cn/mw690/3c1b9c69ly1fq9w3muwugj20gt0gr74n.jpg)  
&emsp;&emsp;我们可以看出，由于使用SAX的方式读取xml是一行一行的，十分的繁琐，效率也是十分的地下，要使用还需要通过对字符串的一系列操作才能较好地使用，所以正常情况下能用json的方式还是用json的方式吧。