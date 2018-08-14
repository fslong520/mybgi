---
title: 03-删除顽固文件方法之借尸还魂
date: 2018-04-07 05:02:46
categories: study
tags: [Win10,删除,顽固文件]
toc: true
---
&emsp;&emsp;我们有时会遇到这样的文件或文件夹，在资源管理器中可以看见他在那，但是删除的时候又提示“找不到该项目。该项目不在XXX中。请确认该项目的位置，然后重试”，这种情况大多数是文件确实已经删了，但资源管理器没刷新，你以为他在，结果他不在了已经，所以报错。但也有少数情况**看得见那个文件，但删除的时候提示他不在，点击取消刷新过之后那个文件还在那，十分的顽固，**本文提供了一种删除的办法，不保证一定好用，但如果遇到了类似情况，不妨试下，万一成功了呢。  
&emsp;&emsp;由于笔者是之前遇到这个问题，当时也截图了，但不完全，现在使用另外一种方法制造了个假的提示，如下图：  
![删除文件时报错](https://fslong.coding.me/blog/images/study/03/0.png)  
&emsp;&emsp;就是这种提示，相信有一些朋友也遇到过，下面我们使用的办法是“借尸还魂大法”，原理很简单（划重点）：“**既然提示不存在，那我就新建一个同名的文件借尸还魂，然后再删除。**”  
&emsp;&emsp;笔者当时产生这个问题的原因是使用了某国产垃圾清理软件，造成了好几个Windows.old文件夹无法清除，困扰了若干个月。我是在Win10的Linux子系统下删除的这文件（Windows下也可以，当时删除了好几个这文件，Windows下的忘记截图了）：
### 1. 删除报错：  
<!--more-->
![删除文件时报错](https://fslong.coding.me/blog/images/study/03/1.jpg)![删除文件时报错](https://fslong.coding.me/blog/images/study/03/2.jpg)  
### 2. 点击又进不去：  
![进不去](https://fslong.coding.me/blog/images/study/03/3.jpg)  
### 3. 新建同名文件夹（借尸还魂）：  
![新建同名文件夹](https://fslong.coding.me/blog/images/study/03/4.jpg)  
此时会申请权限，并询问是否覆盖，当然选择是了（Windows下请将文件所有者改为Everyone，并给予完全控制权限）。  
![给予权限](https://fslong.coding.me/blog/images/study/03/5.jpg)  
### 4. 删除文件夹：  
![删除文件夹](https://fslong.coding.me/blog/images/study/03/6.jpg)![删除完成](https://fslong.coding.me/blog/images/study/03/7.jpg)![世界清静](https://fslong.coding.me/blog/images/study/03/8.jpg)  
&emsp;&emsp;至此删除文件完成，本办法无法保证一定奏效，主要针对这两种情况：**1、可以获取这个文件夹的权限；2、删除时提示文件不存在，删除后又自己出现。**如遇到类似情况，不妨一试。  
  

