---
title: 04-获取Bing每日美图并保存到本地
date: 2018-04-09 12:03:13
categories: study
tags: [Python,Json,Bing美图]
toc: true
---
&emsp;&emsp;本文介绍了两种方法来解析本日的必应美图Json数据，并下载图片到本地，当然使用的是Python。  
### 1. 获取Bing每日美图的Json数据  
&emsp;&emsp;通过查阅资料，我们发现``https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1``这个网址可以返回当天的必应美图的Json数据。  
&emsp;&emsp;其中``format=js``表示返回值是Json格式的；``idx=0``表示获取的是今日的,如果设置成1则表示获取的是昨天的，以此类推；``n=1``表示获取几天的，如果``idx=0&n=2``就表示获取昨天和今天的Json。  
下面上代码：  

    from urllib.request import urlopen,urlretrieve
    from contextlib import closing
    import os,re,json
    with closing(urlopen('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')) as page:
        for line in page:
            picUrl+=line.decode('utf-8')

&emsp;&emsp;上述代码引入了urllib.request的urlopen模块和urlretrieve模块，其中urlopen模块用于打开网页，urlretrieve模块用于存储文件到本地，closing模块用于更方便的打开关闭网页（释放资源等）。  
&emsp;&emsp;``with closing``那一行的意思是通过后面的urlopen函数打开那个网页，然后在用完之后关掉，释放掉。后面两行是将byte型的网页数据合并存储成string。  
### 2. 解析数据  
&emsp;&emsp;这里解析数据有两种，一种是通过Json来解析数据，另外一种是通过正则表达式来解析。
#### 2.1 使用Json解析数据  
先上代码：  

    a=json.loads(picUrl)#将字符串序列化成json
    realPicUrl='https://www.bing.com'+a['images'][0]['url']#获取真实的图片链接
    picPath=os.path.join(os.path.realpath('.'),a['images'][0]['enddate']+'.jpg')#获取本地目录并设置为图片保存目录
&emsp;&emsp;通过观察获取到的Json数据，发现他是一个dict套着一个list里面再套着一个dict，如图：  
![返回的Json](https://wx1.sinaimg.cn/mw690/3c1b9c69ly1fq6ofod6wwj20qk0dmta7.jpg)
&emsp;&emsp;所以当我们把获取到的数据序列化成Json之后就可以使用``a['images'][0]['url']``来取得相对地址，然后再在前面添加上``https;//www/bing.com``就是完整的图片地址。第三行语句是设置一个用于保存图片的地址，目录是程序执行的目录，名字就用该图片的日期。  
#### 2.2 使用正则表达式解析数据  
&emsp;&emsp;通过仔细观察，我们也能使用正则表达式来实现该功能，具体大家的想法可能都不太一样，反正都是字符串的操作，我贴上我的：  

    realPicUrl='https://www.bing.com'+re.match(r'^(.*)(url)(\":\")(.*\.jpg)(.*)$',picUrl).group(4)
    picPath=os.path.join(os.path.realpath('.'),re.match(r'^(.*)(enddate)(\":\")(.*)(\"\,\"url\")(.*)$',picUrl).group(4)+'.jpg')  
&emsp;&emsp;含义也是跟前面一样，没啥好解释的，有一点需要注意，拼接文件地址的时候不要直接``+``，要用``os.path.join(a,b)``，这是因为不同系统的用的标识符不一样。  
### 3. 保存图片  
&emsp;&emsp;只有一行代码，很简单：``urlretrieve(realPicUrl,picPath)``realPicUrl是前面通过解析得到的必应每日美图的真实地址，而picPath刚刚设置好的保存位置及名称。执行完之后就可以看到文件夹里多了一张图片：  
![](https://wx4.sinaimg.cn/mw690/3c1b9c69ly1fq6otiqms8j209s08eaaq.jpg)
### 4. 总结  
&emsp;&emsp;上述代码跟原理都很简单，如果是比较熟练使用正则表达式的老司机用正则表达式的方式更快捷方便一些，而且对于抓取网页数据，正则表达式相对还是方便一些；但单纯的针对本例子，用Json的方法会更好更快捷一些，而且后续如果要获取多条数据，正则表达式的局限性马上就出现了，所以对于能够序列化成Json的，其实最好还是序列化成Json，不容易翻车。
  
   
   
       