---
title: 09-Windows10下的Django WebAPP开发环境搭建
date: 2018-05-31 14:49:05
categories: study
tags: [Python,Coding.net,Linux,Windows10]
toc: true
--- 
<p class = "uk-text-right"><i>本文记录了本人使用Django开发WebAPP时环境的搭建以及一些示例代码。</i></p> 

首先我们为什么要在Windows10下开发呢？个人总结了以下几个优点：   

1. Windows10自身良好的使用环境，包括经常用到的一些APP都十分的成熟、便利，个人认为，日常使用，Windows10还是很舒服的，如果我们工作、开发(涉及到Linux方面)也能在上面那就更好了；
2. Windows10目前Linux子系统与Windows10系统文件互通性已经非常好。在这里，皮一下使用数据库的名词，文件的“增删改查”，在两个系统都能实时的更新，只要文件在一个系统上保存，另外一个系统实时也会更改，十分的便捷；
3. 相比而言，使用Windows系统的用户毕竟是多数，我们在测试的时候，Windows环境的测试是必须的，这时候，用自己电脑直接测试，也是十分的方便；
4. Windows下的开发工具相对而言还是比较多，比较好用的；
5. 大部分关于部署的教程都是Linux的，如果没有WSL(Linux子系统)我们在Windows10下面开发完，再部署那是相当的麻烦，WSL的诞生完美的解决了这个矛盾，将两个系统的优点结合在一起了；
6. 最后那就是信仰了，微软大法好。  

言归正传，下面开始介绍：  
### 目录  
####  [01-Linux子系统的安装](#1)  
####  [02-Django学习](#2)  
---
为了方便介绍，下文中Linux子系统操作用WSL代替，Windows下操作用Win32代替。
<h3 id="1">01-Linux子系统及Win32下VS Code的安装</h3>   

这部分详见我的另外一篇文章：[01-Windows10 Linux子系统安装图形化界面的两种方法及其对比](#1)。本文因为要同时使用Linux子系统和Windows10，所以使用的是Xming的方法。为了巩固记忆以及叙述方便，我又新安装了一个Ubuntu1804来进行演示(平时使用的是Debian，今天顺便也体验下新的Ubuntu系统)。安装好界面如下：  
![Ubuntu1804](https://i.loli.net/2018/05/31/5b0fa9292f9d3.png)
<!--删除链接：https://sm.ms/delete/P1CeGbhJHQu3cmp -->
下面安装xfce4等一系列安装完系统之后的配置，以及Win32下安装VS code的操作，相关内容很简单，傻瓜式安装，可以参考其他文章。
<h3 id="2">02-Linux子系统工作环境的搭建</h3>  

一、安装虚拟工作空间：     
如果一台机器上要建立多个项目，每个项目又使用不同的程序版本，这就需要我们使用虚拟工作空间，为不同的项目安装不同版本的程序；  
我们推荐使用`virtrualenv`以及`virtrualenvwrapper`这个虚拟工作工具管理工具来进行虚拟工作空间管理，安装代码：`sudo apt-get install virtrualenvwrapper`  
二、配置虚拟工作空间：
1. 有几个关于虚拟工作空间的常用指令需要记录下(Ubuntu的问题好多，又用回了Debian)：**创建工作空间**：`mkvirtrualenv <workSpaceName>`; **删除工作空间**：`rmvirtrualenv <workSpaceName>`; **进入工作空间**：`workon <workSpaceName>`;**退出工作空间**：`deactivate` 下面我们先创建一个工作空间，名为`django2.0.5`：  
 ![2.png](https://i.loli.net/2018/05/31/5b0fb5ab97795.png)<!-- 删除链接https://sm.ms/delete/D8S9itZd5hLIuJa -->
2. 进入虚拟工作空间并新建Django项目(注意django对于python的版本支持):我们今天选择2.0.5版本进行安装： **安装django**：`pip install django===2.0.5`，也可以使用`pip list`来查看安装了哪些模块。![3.png](https://i.loli.net/2018/05/31/5b0fb765e5b78.png)  
到此为止，django的工作环境配置完毕<!--删除链接 https://sm.ms/delete/1y4N9wAthERQ5qo -->
三、创建并编写项目：
1. 在WSL下，在刚刚建立的环境下，cd到你想要的目录下(我这里直接在OneDrive目录下创建的，工作和家庭电脑自动同步，美滋滋！)，运行`django-admin startproject <projectName>`，这样就生成了一个新的工程，我们可以打印目录看看：
2. 在Win32下编写hello word页面：
3. 在WSL下测试运行：
4. 使用apache2进行部署：