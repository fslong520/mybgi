---
title: 11-Debian9安装MariaDB(MySQL)及其配置
date: 2018-07-11 19:05:09
categories: study
tags: [Python,Linux,Windows10]
toc: true
--- 
<p class = "uk-text-right"><i>本文记录了笔者在Win10的Linux子系统下安装MariaDB并进行配置的过程。</i></p> 
&emsp;&emsp;笔者的开发环境是Windows10，部署使用的是Windows10的Linux子系统（WSL），这样省了很多麻烦，前面的文章也介绍过类似的的内容，这里不再赘述。顺便提一下，目前Linux子系统已经有很多，包括有Ubuntu、openSUSE、SUSE Linux、Debian、Kali等，笔者由于习惯的原因，使用的是Debian。由于项目以及学习需要，最近安装了MariaDB，把安装过程及遇到的坑记录下。    

![在Windows上运行Linux.png](https://i.loli.net/2018/07/11/5b45e5daa1914.png)<!--删除链接：https://sm.ms/delete/4DBvj6ZL39XcprH -->  

### 一、MariaDB简介  
#### 引用百度百科及其他相关资料:
> MariaDB数据库管理系统是MySQL的一个分支，主要由开源社区在维护，采用GPL授权许可。MariaDB的目的是完全兼容MySQL，包括API和命令行，使之能轻松成为MySQL的代替品。在存储引擎方面，使用XtraDB（英语：XtraDB）来代替MySQL的InnoDB。MariaDB由MySQL的创始人Michael Widenius主导开发，他早前曾以10亿美元的价格，将自己创建的公司MySQL AB卖给了SUN，此后，随着SUN被甲骨文收购，MySQL的所有权也落入Oracle的手中。MariaDB名称来自Michael Widenius的女儿Maria的名字。MySQL之父Widenius先生离开了Sun之后，觉得依靠Sun/Oracle来发展MySQL，实在很不靠谱（**有闭源风险**），于是决定重新开发代码全部开源且免费的关系型数据库，这就是MariaDB的由来。   

&emsp;&emsp;目前Debian的软件源里已经由MariaDB来代替MySQL，我们要使用MySQL的话安装MariaDB即可。
### 二、安装MariaDB
&emsp;&emsp;同安装其他软件一样两行代码（甚至与安装MySQL的方式类似）：  
```
sudo apt-get update
sudo apt-get install mariadb-server
``` 
### 三、启动MariaDB服务
&emsp;&emsp;这里需要使用MySQL的命令，而且要在root权限之下：`sudo service mysql start`（启动服务）或者`sudo service mysql restart`（重启服务），如果不报错的话如下图：  
![启动MariaDB服务.png](https://i.loli.net/2018/07/11/5b45ec9def61f.png)<!--删除连接：https://sm.ms/delete/ZYFCXrbGNDz7BOn-->  
&emsp;&emsp;此时我们可以输入`sudo service mysql status`来查看是否成功启动，如果成功启动：  
![成功启动MariaDB服务.png](https://i.loli.net/2018/07/11/5b45ed228ecf6.png)<!--删除链接：https://sm.ms/delete/cSoPkqwEpIsLeFx-->    
&emsp;&emsp;如果未能成功启动是这样的：  
![未能成功启动MariaDB服务.png](https://i.loli.net/2018/07/11/5b45ed73b91c3.png)<!--删除链接：https://sm.ms/delete/SX8tm6hfnc9yJP1-->  
&emsp;&emsp;如果没成功启动，那就需要再试试前面的命令，以及根据相应报错查阅资料再进行处理了，这里如果按照上文所说操作应该不会有任何问题。  
### 四、在终端启动MariaDB命令行并创建数据库TESTDB进行测试
1、 输入`sudo mysql -u root -p`然后输入root账户的密码（未启用root账户的话是sudo超级管理员密码）启动MariaDB命令行（**注意，一定要在服务启动的情况下输入本命令，不然会报错`Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' `只有MariaDB服务在运行的时候，才会有mysqld.sock这个文件存在**）:  
![成功启动MariaDB命令行.png](https://i.loli.net/2018/07/11/5b45eff246adb.png)<!--删除连接：https://sm.ms/delete/odzCeuyKXHFTIs3-->
2、 输入SQL语句`CREATE DATABASE TESTDB`来创建数据库`TESTDB`，并测试：  
![成功添加数据库跟数据表.png](https://i.loli.net/2018/07/11/5b45f2a366728.png)<!--删除链接：https://sm.ms/delete/6xu21OWpQNHmdSk-->  
&emsp;&emsp;如果跟我的运行结果一样，那说明成功了，下面就是用其他程序连接并驱动数据库了。
### 五、使用pymysql连接MariaDB数据库
1、 首先需要安装pymysql，代码是`sudo pip3 install pymysql`;  
2、 连接数据库，我们在这里使用了预先写好的代码：  
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 学习MariaDB数据库 '

__author__ = 'fslong'

import pymysql
# 打开数据库链接：
db = pymysql.connect(host='127.0.0.1', port=3306,
                     user='root', passwd='passwd', db='TESTDB')
# 建立游标：
cursor = db.cursor()
# 预设sql语句：
sql = """CREATE TABLE EMPLOYEE (
        FIRST_NAME CHAR(20) NOT NULL,
        LAST_NAME CHAR(20),
        AGE INT,
        SEX CHAR(1),
        INCOME FLOAT,
        PRIMARY KEY (FIRST_NAME))ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
# 使用execute()驱动数据库并执行语句：
try:
    cursor.execute(sql)
    # 提交到数据库执行：
    db.commit()
except:
    # 如果发生错误则回滚：
    db.rollback()
# 关闭数据库链接：
db.close

```
3、 在终端中运行`sudo python3 testDB.py`，不出意外的话会出错：  
![pymysql连接MariaDB出错.png](https://i.loli.net/2018/07/11/5b45f4b283524.png)<!--删除连接：https://sm.ms/delete/513kyeJIOTuQhGj-->  
&emsp;&emsp;这里是localhost端口权限问题导致的报错，我们回到MariaDB命令行终端使用`grant`授权命令给予权限即可，完整代码`grant all on TESTDB.* to root@localhost identified by “passwd″;`（grant 后面的all指的是增删改查所有命令，你也可以只给部分权限，详细资料请看参考文献）然后再执行Python代码，之后我们查看下tables，一切正常，如下：  
```
MariaDB [TESTDB]> SHOW TABLES;
+------------------+
| Tables_in_TESTDB |
+------------------+
| EMPLOYEE         |
| test1            |
+------------------+
2 rows in set (0.00 sec)
```
4、 我们尝试使用pymysql插入数据，这次我们再封装个类专门用于执行mysql语句（比较原始的类）：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 学习MariaDB数据库 '

__author__ = 'fslong'

import pymysql


class MySQLConnection(object):
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='passwd', dbName='TESTDB'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName

    def executeSQL(self, sql=''):
        if sql == '':
            # 预设sql语句：
            sql = """CREATE TABLE IF NOT EXISTS `runoob_tbl`(
                `runoob_id` INT UNSIGNED AUTO_INCREMENT,
                `runoob_title` VARCHAR(100) NOT NULL,
                `runoob_author` VARCHAR(40) NOT NULL,
                `submission_date` DATE,
                PRIMARY KEY (`runoob_id`)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        db = pymysql.connect(host=self.host, port=self.port,
                             user=self.user, passwd=self.passwd, db=self.dbName)
        cursor = db.cursor()
        # 使用execute()驱动数据库并执行语句：
        try:
            cursor.execute(sql)
            # 提交到数据库执行：
            db.commit()
        except:
            # 如果发生错误则回滚：
            db.rollback()
        # 关闭数据库链接：
        db.close

if __name__ == '__main__':
    conn = MySQLConnection()
    sql = """INSERT INTO runoob_tbl(runoob_title, runoob_author, submission_date)
    	VALUES("学习 PHP", "菜鸟教程", NOW());"""
    conn.executeSQL(sql=sql)
```  
&emsp;&emsp;执行两次后，回到MariaDB命令行终端查看：
```
MariaDB [TESTDB]> SHOW TABLES;
+------------------+
| Tables_in_TESTDB |
+------------------+
| EMPLOYEE         |
| runoob_tbl       |
| test1            |
+------------------+
3 rows in set (0.00 sec)

MariaDB [TESTDB]> SELECT * FROM runoob_tbl;
+-----------+--------------+---------------+-----------------+
| runoob_id | runoob_title | runoob_author | submission_date |
+-----------+--------------+---------------+-----------------+
|         1 | 学习 PHP     | 菜鸟教程      | 2018-07-11      |
|         2 | 学习 PHP     | 菜鸟教程      | 2018-07-11      |
+-----------+--------------+---------------+-----------------+
2 rows in set (0.00 sec)

MariaDB [TESTDB]> 
```
&emsp;&emsp;运行正常，以后就可以愉快的玩耍了，上面用pymysql连接MariaDB的代码注释已经比较清楚，主要思路是：`建立连接→建立游标→执行语句→提交更改→关闭连接释放游标`，也算是ORM的雏形，以后我们可以在此基础上拓展功能。最后，感谢群里帮助过我的小伙伴，感谢参考文献，感谢关注。  

---   

#### *参考文献*
> 1、[Python3 MySQL 数据库连接](http://www.runoob.com/python3/python3-mysql.html)  
2、[Mysql中grant命令详解](https://blog.csdn.net/lampsunny/article/details/7410657
)
