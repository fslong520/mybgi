---
title: 14-Python多进程、多线程等对比实验
date: 2018-08-14 14:50:10
categories: study
tags: [Python,Linux,Windows10]
toc: true
--- 
<p class = "uk-text-right"><i>本文对Python使用多线程、多进程、异步IO进行对比</i></p> 
&emsp;&emsp;笔者的开发环境是Windows10，部署使用的是Windows10的Linux子系统（WSL），这样省了很多麻烦，前面的文章也介绍过类似的的内容，这里不再赘述。顺便提一下，目前Linux子系统已经有很多，包括有Ubuntu、openSUSE、SUSE Linux、Debian、Kali等，笔者由于习惯的原因，使用的是Debian。今天对Python使用多线程、多进程、异步IO进行了对比，首先先上代码：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 多进程、多线程、异步io学习 '

__author__ = 'fslong'
__version__ = '0.0.1'

import asyncio
import multiprocessing
import threading, time, queue


def job(j):
    print('子线程/子进程:%s' % (j + 1))
    print('线程数量:', threading.active_count())
    #print('线程:', threading.current_thread())
    for i in range(1000000):
        j += i
    #time.sleep(3)
    return j


def job1(j, q):
    print('子线程/子进程:%s' % (j + 1))
    print('线程数量:', threading.active_count())
    #print('线程:', threading.current_thread())
    for i in range(1000000):
        j += i
    #time.sleep(3)
    q.put(j)
    return j


async def yibu(j, result):
    print('子线程/子进程:%s' % (j + 1))
    print('线程数量:', threading.active_count())
    #print('线程:', threading.current_thread())
    for i in range(1000000):
        j += i
    result.append(j)


def mp():
    pool = multiprocessing.Pool()
    result = []
    for i in range(100):
        res = pool.apply_async(job, args=(i, ))
        result.append(res.get())
    pool.close()
    pool.join()
    return result


def loop():
    q = queue.Queue()
    result = []
    threads = []
    for i in range(100):
        t = threading.Thread(
            target=job1, args=(
                i,
                q,
            ))
        t.start()
        threads.append(t)
    for i in threads:        
        i.join()
        result.append(q.get())
    return result


def yibuIo():
    result = []
    loop = asyncio.get_event_loop()
    task = [yibu(i, result) for i in range(100)]
    loop.run_until_complete(asyncio.wait(task))    
    return result


if __name__ == '__main__':
    
    start1 = time.time()
    i = 0
    while i < 10:
        i += 1
        result = []
        for j in range(100):
            result.append(job(j))
        #print(result)
    end1 = time.time()    

    start2 = time.time()
    i = 0
    while i < 10:
        i += 1
        mp()
        #print(mp())
    end2 = time.time()
    
    
    start3 = time.time()
    i = 0
    while i < 10:
        i += 1
        loop()
        #print(loop())
    end3 = time.time()
    

    start4 = time.time()
    i = 0
    while i < 10:
        i += 1
        yibuIo()
        #print(yibuIo())
    end4 = time.time()
    print('采用单线程执行了10次耗时：%s' % (end1 - start1))
    print('采用多线程执行了10次耗时：%s' % (end3 - start3))
    print('采用多进程执行了10次耗时：%s' % (end2 - start2))    
    print('采用异步IO执行了10次耗时：%s' % (end4 - start4))
    #input()

```
将上面的代码分别在win10的cmd中以及wsl中执行，执行结果（多次执行，结果基本一致）如下图：  
![python多任务对比.png](https://i.loli.net/2018/08/14/5b726e9975f62.png)<!--删除连接：https://sm.ms/delete/PRCcJ1DUykwpVES-->   
笔者电脑cpu是i3 3210m，双核四线程的配置。执行期间观察任务管理器结果如下：  

|         |   单线程  |   多进程  |  多线程   |  异步IO   |
| :------ | :------: | :------: | :------: | :------: |
| cpu占用 |1×30%左右|4×8%左右|1×30%左右|1×29左右|

上表可见这堆代码其实也已经占满了一个核心的计算能力。

### 结论
从上图我们可以看出来以下几点：
1. 在win10下直接执行python脚本速度反而没有在wsl（Linux环境）中快；
2. 单线程在win10和wsl（Linux环境）中运行差别不大；
3. 多线程、多进程、异步io，运行速度wsl（Linux环境）中普遍要比win10中快10%左右，这有可能跟代码有关；
4. wsl（Linux）环境下多线程和多进程速度基本一致，在win10下多线程明显要比多进程快，据大佬解释，Windows环境下多线程能力要强一些，单核性能十分重要，这也就是为何amd的cpu那么多核还被Intel的cpu吊打的原因，实验结果也符合预期结果；
5. 由于Python的语言特性，异步IO没有多线程任务切换期间的资源消耗，导致使用异步IO实现多并发执行速度最快，win10和wsl（Linux环境）均有如此结果，尤其是在wsl（Linux）环境下尤为突出，比单线程速度提升大约15%。  

### 思考
1. 上述代码主要是多任务类型，有大量的IO吞吐，而不是计算密集型，由于Python有gil锁，导致多线程以及异步IO只能利用一颗CPU，这种情况下使用异步IO有很大的优势，实际工程中比如网络应用之类主要就是这种类型；
2. 如果遇到计算密集型，比如迭代，科学计算，矩阵，神经网络计算之类的，如果还使用一个核的话浪费了太多资源，这时就可以体现出多进程的优势；
3. 如果追求最大限度的性能，可以使用**多进程+异步IO**结合的方式。 