---
title: 01-Windows10 Linux子系统安装图形化界面的两种方法及其对比
date: 2018-04-05 11:24:24
categories: study
tags: [linux,Win10,bash,GUI]
toc: true
---
&emsp;&emsp;理论上讲，所有Win10的Linux子系统都可以通过Windows10本机远程桌面和Xming的方法来安装使用图形化界面，笔者目前只接触了Debian系的Linux系统，故以Debian GUN/Linux系统和xfce4为例介绍（Ubuntu系统装完Xming就能使用，在此不再叙述，详情请关注IT之家极客学院，同时本文也是为了方便一些有一定Linux使用经验朋友而写的，不喜勿喷）。另外，如果是Linux使用比较多的话，笔者推荐使用Debian系统，稳定性、依赖方面强过Ubuntu及Kali Linux等。   
# 1 使用Windows10本机远程桌面连接   
&emsp;&emsp;顾名思义，这种方法的原理是Linux子系统通过Xrdp启动一个远程连接的服务，打开本机一个端口，然后Windows10系统再启动远程桌面连接这个端口，通过这种方式来启动Linux子系统上面的桌面应用。   
&emsp;&emsp;为了方便起见，笔者也编辑好了sh脚本供各位参考(推荐更新完软件源再使用，从安装Xorg到配置Xrdp全在这个sh脚本里，脚本如何使用请自行百度)：[右键另存sh文件](./files/bash.sh)   
## 1.1 首先安装好Debian   
&emsp;&emsp;具体过程不在叙述，参见[IT之家Win10使用进阶：一周年更新14316如何开启Linux Bash命令行](https://www.ithome.com/html/win10/216665.htm)，安装好并设置密码之后如下：   
![安装好Debian](https://fslong.coding.me/blog/images/study/01/1.png)   
<!-- more -->
## 1.2 使用国内软件源   
&emsp;&emsp;众所周知的原因，在国内如果使用官方源的话，更新软件、安装软件会非常的慢，非常痛苦，我们需要替换成国内软件源（有些老司机有比较好的国外源或是不喜欢国内源有大把时间等待的，可以跳过此步）：   
1.2.1 在win10资源管理器中打开``C:\Users\username\AppData\Local\Packages\TheDebianProject.DebianGNULinux_76v4gfsz19hv4\LocalState\rootfs\etc\apt``文件夹（将username替换为你自己的win10账户名）。   
1.2.2 编辑sources.list文件，用#号注释掉原有的官方更新源，增加国内源。下面我贴出中科大比较稳定的stretch分支的源，软件比较老，但是稳定。然而我个人用的是buster分支，软件比较新，有些奇怪的事，Ubuntu默认用的很多软件的版本就比较新，所以系统稳定性要比Debian差些，求稳的同志们就用下面的源吧：      
    
    deb https://mirrors.ustc.edu.cn/debian/ stretch main contrib non-free   
    deb-src https://mirrors.ustc.edu.cn/debian/ stretch main contrib non-free   
    deb https://mirrors.ustc.edu.cn/debian/ stretch-updates main contrib non-free   
    deb-src https://mirrors.ustc.edu.cn/debian/ stretch-updates main contrib non-free   
    deb https://mirrors.ustc.edu.cn/debian-security/ stretch/updates main contrib non-free   
    deb-src https://mirrors.ustc.edu.cn/debian-security/ stretch/updates main contrib non-free   
笔者在此也放出中科大大佬的工具，上面有常用的Linux发行版的国内源文件，已经设置好的，供各位下载：[点击访问](https://mirrors.ustc.edu.cn/repogen/)   
1.2.3 编辑完保存，如图：   
![软件源列表](https://fslong.coding.me/blog/images/study/01/2.png)   
## 1.3 更新软件源   
代码：`` sudo apt-get update``   
![更新软件源](https://fslong.coding.me/blog/images/study/01/3.png)   
**注意：这里有个坑，因为是https协议的，但Win10的Debian子系统，并没有安装apt-transport-https，直接更新会报错，建议第一次更新先使用http协议或者官方源，在装完apt-transport-https之后，再使用1.2中https协议的软件源（Debian的buster以上分支也不需要，stable类的分支必须先安装apt-transport-https才能使用https协议的软件源，使用https协议可以有效防止运营商劫持）。**   
更新完如图：   
![更新完软件源](https://fslong.coding.me/blog/images/study/01/4.png)   
如果更新完报错：   
![更新报错](https://fslong.coding.me/blog/images/study/01/5.png)   
输入代码：``sudo echo 'apt::sandbox::seccomp "false";' > /etc/apt/apt.conf.d/999seccomp``可以解决    
## 1.4 安装Xorg    
&emsp;&emsp;xorg是xfce桌面需要的一个基础依赖性质东西，开机时候提供登陆界面。这里我说的可能不太准确，个人理解就是要装xfce必须先安装xorg，不然使用起来会有些问题，比如缺少这个组件那个组件的，如果装Ubuntu桌面的话替换成kdm，xfce也可以先装xdm，看个人喜好。    
代码：``sudo apt-get install xorg``大约需要361M空间   
![安装xorg](https://fslong.coding.me/blog/images/study/01/6.png)   
选择语言区域（建议选英文，选汉语也没用，就当学英语了），一路回车：   
![选择语言区域](https://fslong.coding.me/blog/images/study/01/7.png)    
## 1.5 安装xfce4   
代码：``sudo apt-get install xfce4``此处大约需要441M空间，如果不换国内源的话怕是需要下载一天。   
## 1.6 安装并配置Xrdp   
&emsp;&emsp;Xrdp允许Windows或Linux系统通过远程桌面的方式来访问另外一台主机，特别适合本地虚拟机使用，详情参考Linux公社文章：[xrdp完美实现Windows远程访问Ubuntu 16.04](https://www.linuxidc.com/Linux/2017-09/147112.htm)。   
1.6.1 安装Xrdp，代码：``sudo apt-get install xrdp``   
![安装Xrdp](https://fslong.coding.me/blog/images/study/01/8.png)
1.6.2 设置3390端口   
在这里设置以后访问远程连接的端口：   
代码：``sudo sed -i 's/port=3389/port=3390/g' /etc/xrdp/xrdp.ini``   
![设置3390端口](https://fslong.coding.me/blog/images/study/01/9.png)  
1.6.3 设定启动的桌面   
&emsp;&emsp;我们需要告诉远程连接启动的时候启动哪个APP，不然远程桌面连接会黑屏（有很多小伙伴第一次玩这个的时候都有这问题）：   
代码：``sudo echo xfce4-session >~/.xsession``   
1.6.4 重启Xrdp服务   
&emsp;&emsp;此刻还尚未启动服务，远程桌面无法连接，个人也没搞明白，为什么要用重启的命令，试过启动的命令，报错了。   
代码：``sudo service xrdp restart``   
![重启Xrdp服务](https://fslong.coding.me/blog/images/study/01/10.png)   
&emsp;&emsp;此时有可能会有请求通过防火墙的提示，自然是要选择允许才行，另外，值得注意的是，每次开机都得重启启动Xrdp服务，也可以加入启动项，这里不展开叙述。   
## 1.7 启动远程桌面   
1.7.1 在Cortana中搜索远程桌面并启动   
![搜索远程桌面](https://fslong.coding.me/blog/images/study/01/11.png)   
1.7.2 点击显示选项，填入本机IP（这里是局域网IP，所以你也可以用局域网内其他Windows10电脑试试）、刚刚设置的端口号、还有你的Linux子系统用户名（也可以使用root账户登陆，比较麻烦，因为Debian默认是禁止使用root账户登陆的，需要先给root账户设置一个密码``sudo passwd root``），如图：   
![搜索远程桌面](https://fslong.coding.me/blog/images/study/01/12.png)   
1.7.3 点击连接   
![连接远程桌面](https://fslong.coding.me/blog/images/study/01/13.png)   
![连接远程桌面](https://fslong.coding.me/blog/images/study/01/14.png)   
1.7.4 输入Linux子系统密码   
![输入密码](https://fslong.coding.me/blog/images/study/01/15.png)   
1.7.5 尽情享（shí）用吧   
![享用](https://fslong.coding.me/blog/images/study/01/16.png)   
![享用](https://fslong.coding.me/blog/images/study/01/17.png)   
至于后面需要做的配置，参见：[debian 9 安装后需做的几件事](https://www.cnblogs.com/OneFri/p/8308340.html)。   
# 2 使用Xming及ssh连接   
&emsp;&emsp;如果你用的Windows10子系统是Ubuntu，那安装完就能用了，很简单的详见IT之家相关教程，理论上所有Linux都可以通过本方法来实现安装，下面是Debian以及Kali Linux等系统需要做的配置，参考了：[Use SSH and XMing to Display X Programs From a Linux Computer on a Windows Computer](http://www.instructables.com/id/Use-SSH-and-XMing-to-Display-X-programs-from-a-Lin/)。   
&emsp;&emsp;首先需要安装Debian还有xfce4，与上面第一种方法述1.1至1.5的内容完全一致，在此不再赘述，安装好之后进行如下操作：   
## 2.1 安装xming   
没什么特殊的，下载安装，打开就行，地址：[https://xming.en.softonic.com/?ex=REG-60.2](https://xming.en.softonic.com/?ex=REG-60.2)   
## 2.2 确定OpenSSH已经安装   
在终端执行：``sudo apt-get install openssh-server``   
要是如下图这样，那就是没有安装，输入y确认就是了：   
![确认安装了OpenSSH](https://fslong.coding.me/blog/images/study/01/18.png)   
## 2.3 配置DISPLAY方法运行变量   
&emsp;&emsp;安装完xming之后你会发现并不能像Ubuntu一样运行	DISPLAY=:0 startxfce4指令来启动Debian的应用程序，提示找不到DISPLAY方法，那是没有配置ssh相关内容，我们需要做如下配置：   
2.3.1 打开``${HOME}/.bashrc``文档，在最后面加入：   
   
    if [ -d "${HOME}/bin" ] ; then
        export  PATH="${PATH}:${HOME}/bin"
        if [ -f "${HOME}/bin/ssh_login" ] ; then
            . "${HOME}/bin/ssh_login"
        fi
    fi   
 2.3.2 在``${HOME}/bin/``文件夹下新增``ssh_login``文件（bin文件夹没有就新建一个），内容如下：   
   
    if [ -n "${SSH_CLIENT}" ] ; then
        if [ -z "${DISPLAY}" ] ; then
            export DISPLAY='localhost:10'
        fi
    fi
2.3.3 给ssh_login文件777权限，代码：``sudo chmod 777 ${HOME}/bin/ssh_login``   
![配置SSH](https://fslong.coding.me/blog/images/study/01/19.png)    
![配置SSH](https://fslong.coding.me/blog/images/study/01/20.png)    
![配置SSH](https://fslong.coding.me/blog/images/study/01/21.png)    
## 2.4 在终端中启动xfce4桌面   
&emsp;&emsp;如果你没有配置xming，没改里面东西，那默认实在0号显示器上显示Linux系统的程序，输入代码：``DISPLAY=:0 startxfce4``   
也可以直接启动root账户：   

    sudo su
    DISPLAY=:0 startxfce4
默认状态会只有两个比较简陋的panel，如下图：   
![Xfce4主界面](https://fslong.coding.me/blog/images/study/01/22.png)   
&emsp;&emsp;你也可以再进行拖动调整，比如笔者上面是Windows10的任务栏，下面是Debian的panel，结合到一起美滋滋：   
![笔者的Xfce4](https://fslong.coding.me/blog/images/study/01/23.png)    
&emsp;&emsp;其实正常状态下，还会启动一个桌面进程的，由于我用的是buster分支的软件源，这就导致软件不是最稳定版本，然后desktop启动失败，于是就剩下这两个panel，然而因祸得福，个人感觉这样很舒服，所以保留了这种，如果你用了我上面写的源，启动后的将会和前面的远程桌面类似。   
# 3 Win10远程桌面与Xming连接的对比   
&emsp;&emsp;其实实现原理都比较接近，都需要配置一系列东西，但两者体验还是有些不一样的，下面做个简要的对比：   
## 3.1 安装难易度   
&emsp;&emsp;个人感觉，就Debian来讲使用Xming的方式安装稍微简单一些，但二者相差不多，如果是Ubuntu，那会更加简单，各位可以自行体验。   
## 3.2 启动便携性   
**相同点是：**两者都需要先在powershell或者cmd中先启动bash。   
**不同点是：**远程桌面的方法启动bash后再启动远程桌面，只用配置一次，以后点击链接就可以，相当于每次启动需要鼠标点击一次powershell，输入bash，点击远程桌面，点击链接；   
&emsp;&emsp;Xming的方法需要再启动xming，然后在powershell里输入DISPLAY=:0 starxfce4，但是终端都会记录以前输入的内容，所以也不用每次都输入，其实就我个人而言，xming的方法更加方便启（zhuang）动(bi)，哪怕每次都输入``DISPLAY=:0 startxfce4``。   
&emsp;&emsp;使用远程桌面的方法启动后，可以关掉powershell了，只要后台服务在运行，就不会影响体验，但是xming不行，如果刚刚那个启动xfce4的powershell关掉，所有打开的窗口都会关闭。   
## 3.3 使用体验   
&emsp;&emsp;采用远程桌面连接的方式，将会有非常完整的沉浸式体验，你会获得一个完整而不割裂的Linux系统，如在电脑上单独安了一个完整的Linux体验：   
![运行界面1](https://fslong.coding.me/blog/images/study/01/24.png)   
&emsp;&emsp;而使用xming的方法，你会感觉两个系统合二为一了，有种混血儿的感觉，每一个Linux程序都将会开启一个xming窗口，而且这些窗口也支持win10的分屏功能：   
![运行界面2](https://fslong.coding.me/blog/images/study/01/25.png)   
![运行界面3](https://fslong.coding.me/blog/images/study/01/26.png)   
## 3.4 资源占用情况   
&emsp;&emsp;在启动Linux子系统后只开一个文件管理器的情况下，使用远程桌面的方法资源占用稍多，个人猜测可能是远程桌面本身占用的资源稍多一些（实际上Xfce4本身占用的内存已经在bash进程里，看不见详细的占用情况），另外说一下，两者是可以同时打开的：   
![资源占用情况](https://fslong.coding.me/blog/images/study/01/27.png)
## 3.5 与Windows10的互通性   
&emsp;&emsp;**文件互通性：**两者都支持在两个系统下实时更改文件，但是都需要使用root账户登陆才能完全实现实时更改文档，不然在Windows10下的更改，在Linux下看不见，但在Linux下的更改立刻就能在Windows10上看到。   
&emsp;&emsp;**剪贴板互通性：**两者都可以实现剪贴板文本内容的互通，但对于文件就有所不同。如使用远程桌面，文件的话由于两个系统的路径不同，无法从Windows10下粘贴文件到Linux下，如图：   
![复制文件](https://fslong.coding.me/blog/images/study/01/28.png)   
&emsp;&emsp;但是可以从Linux下把文件粘贴到Windows10下的，比如粘贴到桌面，这是通过远程桌面本身实现的，如图：   
![复制文件](https://fslong.coding.me/blog/images/study/01/29.png)   
而如果使用xming的话，只能文本互通，文件无法通过剪贴板复制粘贴，有时候还会有意外发生，需要清空剪贴板，比如笔者就在桌面上放了个![](https://fslong.coding.me/blog/images/study/01/30.png)。   
## 3.6 性能方面   
&emsp;&emsp;个人实际体验，Xming方式的性能较差，比如使用Firefox的时候往往比较卡，这可能是实现方式不同的原因，尝试过提高xming优先级，也没多大用。    
&emsp;&emsp;综上所述，如果希望有完整的沉浸式Linux体验，推荐使用远程桌面连接的方式，如果主要用的还是Windows10，希望使用Windows10的同时也使用Linux，那么笔者推荐使用xming的方式，这种方式可以将两个系统同时结合起来，从而获得很神奇的体验。在此再感谢下参考文献中的大神，有了他们的无私奉献，我们才能学到更多的知识。

---
>**参考文献：**   
[1、Win10使用进阶：一周年更新14316如何开启Linux Bash命令行](https://www.ithome.com/html/win10/216665.htm)   
[2、中科大Debian 源使用帮助](http://mirrors.ustc.edu.cn/help/debian.html)   
[3、使用xrdp实现windows 远程桌面 ubuntu linux](https://blog.csdn.net/daniel_ustc/article/details/16845327)   
[4、debian 9 安装后需做的几件事](https://www.cnblogs.com/OneFri/p/8308340.html)      
[5、Use SSH and XMing to Display X Programs From a Linux Computer on a Windows Computer](http://www.instructables.com/id/Use-SSH-and-XMing-to-Display-X-programs-from-a-Lin/)