---
title: 02-使用Hexo和Coding.net的WebIDE搭建个人博客
date: 2018-04-06 09:49:05
categories: study
tags: [Hexo,Coding.net,博客]
toc: true
---
&emsp;&emsp;作为一条有理想的咸鱼，怎么可以没有个人博客？是时候搭建走一波了，然而目前搭建博客各种方法层出不穷，成本也各不相同。笔者作为一个正在攒老婆本马上要娶小姐姐的小哥哥，只好使用简单粗暴的方法了（其实最主要的就是免费）。   
&emsp;&emsp;Hexo是一个基于Node.js的博客框架，类似于WordPress，官方解释如下：   
![Hexo官方解释](https://fslong.coding.me/blog/images/study/02/1.png)
&emsp;&emsp;Coding.net是一个代码托管网站，类似于GitHub，优点是：这是国内网站，访问速度及稳定性正常情况下都优于GitHub。   
&emsp;&emsp;使用Hexo和Coding.net搭建个人博客的原理其实很简单：将用Hexo生成的网页部署到Coding.net上，然后使用Coding.net的Pages服务生成静态网页。下面开始搞起。   
# 1. 注册Coding.net及升级到银牌会员   
&emsp;&emsp;这部分不详细叙述了，需要升级到银牌会员（有些功能是银牌会员才有的），当然coding上的升级是免费的，腾讯云笔者本身就有买过域名，不清楚光有账号是否还是免费，详见[https://coding.net](https://coding.net)相关说明。   
![升级到Coding银牌会员](https://fslong.coding.me/blog/images/study/02/2.png)
# 2. 建立项目及分支
## 2.1 建立项目   
&emsp;&emsp;登陆以后在个人中心创建新的项目，按自己需要填写圈中的内容，如图：   
![建立项目](https://fslong.coding.me/blog/images/study/02/3.png)
![建立项目](https://fslong.coding.me/blog/images/study/02/4.png)
**注意：**最好勾选启动README.md文件初始化项目，公有或者私有看自己选择，这意味着你的代码是否开源可见，另外为了别人访问方便，建议项目名称起的简单点。
创建好了如下图：   
![建立好项目](https://fslong.coding.me/blog/images/study/02/5.png)
<!-- more -->
## 2.2 创建分支   
&emsp;&emsp;Hexo的写作和部署区是分开的，为了防止项目出一些奇怪的事情，所以需要创建一个专门用于写作的分支，将写作好的项目部署到master分支，之后将master分支部署到静态Pages服务上就可以访问了。   
&emsp;&emsp;点击新建分支：   
![新建分支](https://fslong.coding.me/blog/images/study/02/6.png)
![新建分支](https://fslong.coding.me/blog/images/study/02/7.png)
&emsp;&emsp;分支起点是你从什么分支来创建的这个分支，比如你如果在这里填写master，这个分支建成之后便会和master的内容一样。这里我们要保持不同，所以什么都不填写。创建完如图：   
![新建完分支](https://fslong.coding.me/blog/images/study/02/8.png)
# 3. 使用Coding.net的WebIDE搭建Hexo环境   
&emsp;&emsp;这里需要说明下，你也可以使用本地搭建Hexo环境，因为Coding.net的WebIDE已经搭建好了各种环境，省去了安装Node.js、git、Hexo过程，十分简单粗暴。本文参考了Coding.net大佬的博客：[使用 WebIDE 搭建 Hexo 个人博客。](https://blog.coding.net/blog/webide-hexo)   
## 3.1 启动WebIDE   
先进入项目，选择刚刚创建的分支，点击WebIDE：  
![进入WebIDE](https://fslong.coding.me/blog/images/study/02/9.png)
笔者是个穷人，然后悲剧了，免费帐号只能有一个工作区：   
![只能建立一个工作区](https://fslong.coding.me/blog/images/study/02/10.png)
只好删除之前搭建博客建立的工作区，如下：   
![删除工作区](https://fslong.coding.me/blog/images/study/02/11.png)
![删除工作区](https://fslong.coding.me/blog/images/study/02/12.png) 
回去再次点击WebIDE，这就进去了，如下图：   
![进入WebIDE](https://fslong.coding.me/blog/images/study/02/13.png)
&emsp;&emsp;左侧是文件目录，左下角是终端，右侧是文件编辑区。点击右下角master，选择刚刚建立的分支，点击签出，将本地环境设置成编写博客的分支：   
![切换分支](https://fslong.coding.me/blog/images/study/02/14.png)
![切换分支](https://fslong.coding.me/blog/images/study/02/15.png)
右下角分支变成：![删除工作区](https://fslong.coding.me/blog/images/study/02/16.png)
## 3.2 配置Hexo运行环境   
点击右下角，选择Hexo，点击使用：   
![使用Hexo](https://fslong.coding.me/blog/images/study/02/17.png)
点击左下角终端，新建写作目录并初始化，代码：  
``hexo init <folder>``
其中，folder是你要建立的文件夹的名字，创建有时候比较慢，稍等一会，如图：   
![新建博客目录](https://fslong.coding.me/blog/images/study/02/18.png)
![新建博客目录](https://fslong.coding.me/blog/images/study/02/19.png)  
此时可以点击版本，提交、推送下测试是否正常，比如我这回到原来的代码管理网页就能看到：
![代码管理](https://fslong.coding.me/blog/images/study/02/20.png)
此时在文件树里可以看到：   
![文件树](https://fslong.coding.me/blog/images/study/02/21.png)  
&emsp;&emsp;其中，themes是博客所用的主题，source是届时我们新建或者编辑博客的目录，_config.yml为博客配置文件，在themes文件夹下还有个_config.yml为主题配置文件。
## 3.3 配置信息   
双击myBlog文件夹下面的_config.yml，修改个人信息及配置部署地址，注意冒号后面的空格。   
**首先**，Site字段看个人喜好，title是标题，author是作者：
![Site字段](https://fslong.coding.me/blog/images/study/02/22.png)   
**其次**，url字段是你博客地址：   
![URL字段](https://fslong.coding.me/blog/images/study/02/23.png)  
这个必须填写的，不然到时候有些模块（比如分享）会有问题。   
url是你的博客地址，格式是：``<coding账户名>.coding.me/<项目名>/``   
root是项目名称：``/<项目名>/。``   
**再次**，Directory字段是目录地址，比如我把public_dir改成public/blog,届时生成的博客文件就会在public/blog文件夹下，而不是直接再public下。   
![Directory字段](https://fslong.coding.me/blog/images/study/02/24.png)  
**最后**，deploy（部署）字段，是你要部署的地址，也是必须填写。   
type填写git，然后新增repo和branch，repo填写本项目的ssh地址，可以在项目首页找到（这里先选择SSH，然后再复制）：   
![项目SSH地址](https://fslong.coding.me/blog/images/study/02/25.png) 
branch填写master，这是因为我们最终要部署到master分支上才能通过pages服务部署网页。   
![deploy字段](https://fslong.coding.me/blog/images/study/02/26.png)
# 4. 开始创作   
## 4.1 cd到刚刚建立的目录：``cd myBlog``
![博客目录](https://fslong.coding.me/blog/images/study/02/27.png)
## 4.2 安装依赖项：``npm install``
![安装依赖](https://fslong.coding.me/blog/images/study/02/28.png)
## 4.3 新建博客:``hexo new <title>``  
title是你要新建的博客的标题，如图：   
![新建博客](https://fslong.coding.me/blog/images/study/02/29.png)
``~/workspace/myBlog/source/_posts/Welocome.md``是新建的文件的目录：
![新建博客](https://fslong.coding.me/blog/images/study/02/30.png)
## 4.4 双击刚刚建立的文件，编写博客   
![编写博客](https://fslong.coding.me/blog/images/study/02/31.png)
这里在左边编写，在右边可以实时预览。   
# 5. 生成及部署   
编写好之后就可以发布出HTML文件并部署到master分支了。   
## 5.1 生成   
没啥说的，就一行代码：hexo generate：   
![生成博客](https://fslong.coding.me/blog/images/study/02/32.png)
生成之后，文件树里就会多一个public文件夹，里面就有了index.html网页文件：      
![生成的网页](https://fslong.coding.me/blog/images/study/02/33.png)  
上面代码也可以简写成：``hexo g``
## 5.2 部署   
### 5.2.1 安装git服务依赖：   
``npm install hexo-deployer-git --save``
![安装git服务依赖](https://fslong.coding.me/blog/images/study/02/34.png)
### 5.2.2 配置git   
与本地仓库配置git类似，两行代码（记得替换name和email为自己的信息）：   
配置用户名：``git config --global user.name <name>``   
配置邮箱地址：``git config --global user.email <email>``   
![配置git](https://fslong.coding.me/blog/images/study/02/35.png) 
### 5.2.3 部署   
一行代码：``hexo deploy``   
![部署博客](https://fslong.coding.me/blog/images/study/02/36.png)
之后文件树就会多了.deploy_git文件夹，这个文件夹下面的东西全部会推送到项目的master分支下：   
![文件树](https://fslong.coding.me/blog/images/study/02/37.png)
![代码管理器](https://fslong.coding.me/blog/images/study/02/38.png)
到此为止，我们已经把博客代码推送到了博客项目的master分支下面。   
# 6. 开启Pages服务   
点击项目的Pages服务，选择静态Pages，选择master分支，点击保存：   
![Pages服务](https://fslong.coding.me/blog/images/study/02/39.png)
部署成功则有如下提示：   
![部署成功](https://fslong.coding.me/blog/images/study/02/40.png)
点击已经运行在后面的那个网址就可以访问了：   
![搭建完成的博客](https://fslong.coding.me/blog/images/study/02/41.png)
至此已经完成了博客的生成，以后可以重复4、5两步骤来进行创作以及更新博客。笔者建议在生成之前最好运行Hexo clean清理下Public目录，免得有一些冲突，同时最好有空推送下写作分支的代码到远程仓库，以免丢失数据。另外，官方推荐使用Jekyll来生成静态网页，我后续也会测试下。还有一些比如上传图片、主题、MarkDown语法等等的教程，我会在后续慢慢更新，谢谢大家。 

---

>**参考资料：**   
*[1、使用 WebIDE 搭建 Hexo 个人博客](https://blog.coding.net/blog/webide-hexo)  
[2、Hexo文档](https://hexo.io/zh-cn/docs/index.html)*