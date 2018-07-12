---
title: 06-我的第一只Spider
toc: true
date: 2018-04-12 15:21:36
categories: study
tags: [Python,html,Spider]
---
&emsp;&emsp;在学习完Python的内置模块之后，终于写出来自己的第一只Spider，记录一下！  
&emsp;&emsp;是在廖雪峰老师的博客上看到的题`找一个网页，例如https://www.python.org/events/python-events/，用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。` 
先上效果图： 
![第一只Spider执行结果](https://wx1.sinaimg.cn/mw690/3c1b9c69ly1fq9wvkd3g9j20sg0kiwi2.jpg)
再上代码：
```Python
    from html.parser import HTMLParser
    from html.entities import name2codepoint
    from urllib import request
    import re
    class MyHTMLParser(HTMLParser):
        def __init__(self):# 定义需要使用或者返回的数据
            HTMLParser.__init__(self)# 继承于HTMLParser类，所以初始化的时候需要有这一句
            self.starttag=''
            self.attrs=[]
            self.meetingDict=[]# 用于返回meeting时间和内容的list
            self.i=-1
            self.htmlDict={# 用于返回所以数据的字典
                'starttag':[],
                'endtag':[],
                'startendtag':[],
                'data':[],
                'comment':[],
                'entityref':[],
                'charref':[],
                'attrs':[]
            }
        def handle_starttag(self,tag,attrs):# 用于解析<p>这种标签，也就是起始标签
            self.starttag=tag        
            self.htmlDict['starttag'].append(tag)
            self.attrs=attrs
            self.htmlDict['attrs'].append(attrs)
        def handle_endtag(self,tag):# 用于解析</a>这种标签，也就是闭合标签
            self.htmlDict['endtag'].append(tag)
        def handle_startendtag(self,tag,attrs):# 用于解析<input/>这种标签
            self.htmlDict['startendtag'].append(tag)        
        def handle_data(self,data):# 用于解析啥都没有的字段，就是单纯的文字
            self.htmlDict['data'].append(data.strip())
            data=data.strip()# 去除\n \t \r
            for i in self.attrs:
                if re.match(r'^/events/python-events/\d*/$',i[1]):
                    self.i +=1
                    self.meetingDict.append({})                
                    self.meetingDict[self.i]['event-title']=data
            if self.starttag=='time':
                self.meetingDict[self.i-1]['time']=self.attrs[0][1]# 由于有空白数据产生，导致错位了，通过修正self.i使得date和event-title匹配
        def handle_comment(self,data):# 用于解析注释，也就是<!--test-->
            self.htmlDict['comment'].append(data)
        def handle_entityref(self,name):# 用于解析如&emsp;这种类型元素
            self.htmlDict['entityref'].append('&%s'%name)
            #print('&%s'%name)
        def handle_charref(self,name):# 用于解析&#1234;这种类型元素
            self.htmlDict['charref'].append('&#%s'%name)
            #print('&#%s'%name)
    parser=MyHTMLParser()
    with request.urlopen('https://www.python.org/events/python-events/',timeout=4) as f:
        parser.feed(f.read().decode('utf-8'))
    for i in parser.meetingDict:# 删除event-title的value为空的数据，不知为何会有空白数据产生
        if i['event-title']=='':
            parser.meetingDict.remove(i)
    print(parser.meetingDict)
```
&emsp;&emsp;上面代码的注释已经很详细了，主要步骤跟解析xml感觉差不多（可能是这种方法太低级，相信后续一定有更高级的办法），都是一行一行解析元素标签，这段代码只是一个例子，具体看需要做什么，针对性的返回需要的数据。