---
title: 08-使用Python编写的电子邮件客户端
toc: true
date: 2018-04-23 13:28:45
categories: study
tags: [Python,Email]
---
&emsp;&emsp;本文是根据廖雪峰老师博客所讲的Python教程里的有关电子邮件内容进行了一定的修改整合编写的一套客户端，主要是辅助自己对这块知识更加理解，并编写成了一个类（以后如果需要其实是可以直接调用的），另外就是记录下在编写过程中遇到的坑！  
&emsp;&emsp;其实用Python收发邮件跟我们平时收发邮件逻辑上是一样的（这里就不说那么多深层次原理各位可以参考廖老师博客），**发送邮件的时候**：  
1. 连接邮箱提供商的smtp服务，建立好一个server（相当于登陆邮箱网页并选择自己是126邮箱还是163邮箱），这里需要注意目前邮箱都是要采用加密的，如果采用的是STARTTLS加密模式（outlook等邮箱）需要执行：
    ```python
    server = smtplib.SMTP(smtpAddress, smtpPort) 
    server.starttls()
    ```
&emsp;&emsp;如果采用的是SSL方式加密（163、qq等邮箱）需要执行：``server = smtplib.SMTP_SSL(smtpAddress, smtpPort)``来建立服务，这两种是不一样的，需要去邮箱服务商官网上查看！  

2. 登录邮箱：``server.login(addr, passwd)``；
3. 编辑邮件（我们也可以事先就把邮件编辑好然后再登陆），我直接写了一个editEmail的方法，在此处调用就好；
4. 输入收件人地址；
5. 发送邮件``server.sendmail(addr, self.mailTo, self.msg.as_string())``。 
---  
执行一下看看发送邮件的结果：  
![发送邮件1](http://wx3.sinaimg.cn/mw1024/3c1b9c69ly1fqmlfxr948j20ih0gpq3m.jpg)  
发送完去邮箱里就可以看到刚刚发的邮件：  
![发送邮件2](http://wx1.sinaimg.cn/large/3c1b9c69ly1fqmlg11797j20hj0gdabt.jpg)

<!-- more -->
&emsp;&emsp;看吧，跟平时在网页上发送邮件的逻辑、步骤是一样一样的，**收邮件的时候呢**：  
1. 跟smtp类似，首先建立pop3网络服务：``server = poplib.POP3_SSL(pop3Addres, pop3Port)``，这里需要使用SSL加密协议（目前大部分pop3服务都已经使用SSL加密协议，不使用加密会被拒绝登陆）；
2. 身份认证，这里需要两句代码：``server.user(userAddress)``和``server.pass_(password)``，也就是输入用户名和密码，提交了这两个数据就login上了；
3. 可以使用``server.list()``函数来获取收件箱列表，返回值是一个tuple，第二个参数是收件箱的所有邮件的编号，类似于``[b'1 82923', b'2 2184', ...]``这样的数据，这其实是邮件的索引，'后跟的第一个数字为该邮件的索引，我们可以使用这个数字来读取这封邮件；
4. 下载邮件，此时已经建立好了连接，我们就可以反复调用``server.retr(i)``来获取邮件的内容，返回值也是一个tuple，第二个参数是邮件所有内容，包括header、subject、content等，但此时获取到的数据是二进制数据需要进行解析；
5. 我们可以使用email.parser模块里面的一些方法，对收取到的邮件进行解析！

我们执行一下代码：  
![收取邮件1](http://wx2.sinaimg.cn/mw690/3c1b9c69ly1fqmlg8ozp5j20lt0hn3zy.jpg)
![收取邮件2](http://wx4.sinaimg.cn/mw690/3c1b9c69ly1fqmlg8qe8cj20u90hlmxz.jpg)  
下面上代码：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import os
import pickle
import poplib
import re
import smtplib
import chardet
from email import encoders
from email.header import Header, decode_header
from email.mime.multipart import MIMEBase, MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import formataddr, parseaddr

#############################################################################
# 本客户端提供最简单的邮件收发功能，并可以简单加密保存账户信息到本地，方便第二次登陆
#############################################################################
# 默认未添加任何邮箱服务商的smtp服务器及pop3服务器信息，但你添加过一次之后就会保存
#############################################################################


#############################################################################
#                    本程序是前面写的程序的改写，改成面向对象的
#############################################################################
# 声明一个表示邮箱账户信息的类
class MyEmail(object):
    # 声明这个类的属性，包括账户密码信息，pop3和smtp服务器，所有账户信息
    def __init__(self):
        self.users = []
        self.smtp = {}
        self.pop3 = {}
        self.accounts = {}
        self.selfPassWord = ''
        self.tempSelfPassWord = ''
        self.msg = MIMEMultipart()
        self.mailTo = ''

    # 添加账户信息
    def updateAccounts(self):
        self.accounts['users'] = self.users
        self.accounts['smtp'] = self.smtp
        self.accounts['pop3'] = self.pop3
        self.accounts['selfPassWord'] = self.selfPassWord

    def calculateHash(self, s):
        a = hashlib.sha256()
        a.update(s.encode('utf-8'))
        return a.hexdigest()
    # 检测个人密钥

    def checkSelfPassword(self, s):
        selfPassWord = input('请输入个人密钥用于解密：')
        b = self.calculateHash(selfPassWord)
        if s == b:
            return (True, selfPassWord)
        else:
            return

    # 对密码加密（超级简陋的算法）：
    def encipherData(self, passwd, selfPassWord):
        i = len(passwd) % len(selfPassWord)
        passwd = passwd[0:i] + selfPassWord + passwd[i:-1] + passwd[-1]
        return passwd

    # 对密码解密（超级简陋的算法）：
    def decryptData(self, passwd, selfPassWord):
        decryptedPasswd = ''.join(passwd.split(selfPassWord))
        return decryptedPasswd

    ########################################################################################################
    # 下面是有关发送邮件的方法################################################################################
    ########################################################################################################

    def editEmail(self, addr):
        def _formata_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))
        # 输入收件人地址：
        mailTo = input('请输入收件人地址：')
        # 自定义邮件发送者名称（如果在地址簿中设置了备注，那就不显示）:
        self.msg['From'] = _formata_addr(addr)
        # 自定义收件人名称，接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可（如果在地址簿中设置了备注，那就不显示）：
        self.msg['To'] = _formata_addr(mailTo)
        self.mailTo = mailTo
        # 主题包含中文，所以需要用header格式化一下，主题用Header格式化，address用_formata_addr格式化：

        def subjectOfMail(self):
            subject = input('请输入邮件主题：\n')
            if subject == '':
                print('必须输入主题：')
                subjectOfMail(self)
            return subject

        self.msg['Subject'] = Header(subjectOfMail(self), 'utf-8').encode()

        def attachFile(self):
            # 添加附件
            # 需要把附件转为MIMEBase对象添加上
            # 先从本地打开一个文件：
            a = input('请将文件放到本程序工作目录下，并输入文件名：\n')
            try:
                f = open(a, 'r')
                print('打开附件测试成功，可以发送！')
                f.close()
                # 获取后缀名
                i = a.split('.', 1)[1]
                with open(a, 'rb') as f:
                    # 设置附件的MIME和文件名，这里是jpg类型(第一个参数其实可以随便):
                    mime = MIMEBase(i, i)
                    # 加上必要的头信息，比如content ID回头可以用于在邮件正文中引用
                    # 类型为附件，名称是之前设置过的名称:
                    mime.add_header(
                        'Content-Disposition', 'attachment', filename=a)
                    # 设置ID用于引用等：
                    mime.add_header('Content-ID',
                                    '<' + input('请输入引用时用的id：\n') + '>')
                    #mime.add_header('X-Attachment-Id', '0')
                    # 读取附件并天骄到mime当中:
                    mime.set_payload(f.read())
                    # 将mime使用base64编码
                    encoders.encode_base64(mime)
                    # 添加到MIMEMultipart,往MIMEMultipart添加除Header以外的内容都需要用attach():
                    self.msg.attach(mime)
                a = input('是否继续编辑邮件？y/n\n')
                if a == 'y':
                    chooseContentFunction(self)
                else:
                    pass
            except:
                print('打开附件失败，请重新添加附件!')
                attachFile(self)

        # 增加一个邮件正文内容：
        # 如果把上面的附件，比如上面的照片以html的方法插入到了正文中，将不会在附件中显示
        def attachText(self):
            a = input('纯文本格式请按0，html格式请按1：')
            try:
                a = int(a)
            except:
                a = 0
            b = ('html', 'plain')
            self.msg.attach(
                MIMEText(
                    input('请输入文件正文:\n'), b[a],
                    'utf-8'))  # 邮件文本
            a = input('是否继续编辑邮件？y/n\n')
            if a == 'y':
                chooseContentFunction(self)
            else:
                pass

        # 选择添加什么内容的函数
        def chooseContentFunction(self):
            chooseContent = input('编辑正文请按0，添加附件请按1，退出请按e:\n')
            if chooseContent == '0':
                attachText(self)
            elif chooseContent == '1':
                attachFile(self)
            elif chooseContent == 'e':
                exit
            else:
                chooseFunction()
        chooseContentFunction(self)

    def sendEmailBySmtp(self, addr, passwd, smtp):
        try:
            if smtp[2] == '0':
                server = smtplib.SMTP_SSL(smtp[0], smtp[1])
            else:
                server = smtplib.SMTP(smtp[0], smtp[1])
                print(smtp[0], smtp[1])
                server.starttls()
        except:
            print('建立发送邮件服务失败，请重试！')
        finally:
            if server:
                # 打印调试信息
                #server.set_debuglevel(1)
                print('建立发送邮件服务成功，开始尝试登陆smtp服务器...')
                try:
                    server.login(addr, passwd)
                    print('smtp服务器登陆成功，开始尝试发送邮件...')
                    try:
                        # 发送邮件的时候需要设置msg.as_string()
                        server.sendmail(addr, self.mailTo,
                                        self.msg.as_string())
                        print('邮件发送成功')
                    except:
                        print('邮件发送失败，请重试！')
                except:
                    print('登陆发送服务器失败，请重试！')
    ########################################################################################################
    # 下面是有关接收邮件的方法################################################################################
    ########################################################################################################
    # 邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode：

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 猜一下邮件文本的编码，其实直接导入chardet，就不用了
    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos > 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def parseMail(self, msg, indent=0):
        # Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，嵌套可能还不止一层。
        # 所以我们要递归地打印出Message对象的层次结构：
        # indent用于显示缩进：
        if indent == 0:
            # 获取不同的header的数据：
            for header in ['From', 'To', 'Subject']:
                # 如果header的值是Sbject就解析成主题，使用decode_header来解析(可能存在汉字)
                # 如果不是那一定是发件人或者收件人的地址了，那么就使用parseaddr来解析
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        # 发件人名称有可能也是中文，所有也要用decode_str()方法来decode
                        name = self.decode_str(hdr)
                        if name == 'Frmo':
                            name = '来自'
                        elif name == 'To':
                            name = '收件人'
                        value = u'%s <%s>' % (name, addr)
                        print('%s:%s' % (header, value))
        print('------------------------------------------------------------')
        # 如果msg包含附件：
        if (msg.is_multipart()):
            # 通过观察multipart各个参数的以及对象的数值，发现所有的正文信息都存在payload对象里，所以获取了他并进行分析
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print(
                    '------------------------------------------------------------'
                )
                print('%s<第%s部分>：' % ('  ' % indent, n))
                print(
                    '%s------------------------------------------------------------' % (
                        '  '*indent)
                )
                self.parseMail(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True)
            content = content.decode(chardet.detect(content)['encoding'])
            if content_type == 'text/plain' or content_type == 'text/html':
                #charset = self.guess_charset(msg)
                # 如果猜出来编码，那就decode成那个编码，其实可以直接chardet：
                '''
                if charset:
                    content = content.decode(charset)
                '''
                print('%s<文本>:\n------------------------------------------------------------\n%s' %
                      (('  ' * indent), content + '...'))
            else:
                print('%s<Attachment>: %s/n%s' %
                      (('  ' * indent), content_type, content))

    # 打印邮件标题的函数
    def mailHeader(self, startNum, num, server):
        while startNum > num:
            lines = server.retr(startNum)[1]
            msgContent = b'\r\n'.join(lines).decode('utf-8')
            # Parser()是创立的解析对象，下一步其实是将两部连在一起，先创立一个解析对象，然后再使用Parser类的parsestr()方法解析，返回值是解析完的数据
            msg = Parser().parsestr(msgContent)
            value = msg.get('Subject', '')
            value = self.decode_str(value)
            startNum -= 1
            print('%s、%s' % (startNum + 1, value))


# 设置邮箱账号密码的函数
def setAccounts(myEmail):
    try:
        f = open('pyEmail', 'wb')
    except:
        a = input('文件打开失败，请检查本程序工作目录下的"pyEmail"文件是否占用后重试！\n是否重试建立账户？y/n:')
        if a == 'y':
            setAccounts(myEmail)
        else:
            exit()
    finally:
        if f:
            f.close()
            selfPassWord = input('首次登陆，新建个人密钥：')
            i = input('请输入你要登陆的邮箱地址：')
            j = input('请输入你要登陆的邮箱密码：')
            k = input('请按smtp.example.com:port格式输入smtp服务器及端口：')
            m = input('smtp服务器采用SSL加密请按0，STARTTLS加密请按1:')
            if m == '1':
                m = '1'
            else:
                m == '0'
            l = input('请按pop.example.com:port格式输入pop3服务器及端口：')
            myEmail.selfPassWord = myEmail.calculateHash(selfPassWord)
            myEmail.users.append(
                (i, myEmail.encipherData(j, selfPassWord)))
            myEmail.smtp[i.split('@')[1]] = (
                k.split(':')[0], int(k.split(':')[1]), m)
            myEmail.pop3[i.split('@')[1]] = (
                l.split(':')[0], int(l.split(':')[1]))
            myEmail.updateAccounts()
            with open('pyEmail', 'wb')as f:
                pickle.dump(myEmail.accounts, f)
            print('新账号设置完毕：')
            chooseFunction()

# 读取邮箱账号密码的函数


def readAccounts(myEmail):
    try:
        f = open('pyEmail', 'rb')
        text = f.read()
        print('本地数据读取成功，开始解析...')
        f.close()
    except:
        print('本地数据读取失败，开始新建账户信息数据库...')
        setAccounts(myEmail)
    if text:
        try:
            readAccounts = pickle.loads(text)
            print('本地数据解析成功，开始解密...')
        except:
            print('本地数据解析失败，请重试！')
            chooseFunction()
        if not readAccounts == '':
            checked = myEmail.checkSelfPassword(
                readAccounts['selfPassWord'])
            if checked[0]:
                print('个人密钥验证成功，本地保存的账户有:')
                i = 1
                for j in readAccounts['users']:
                    print('第%s个账户：%s' % (i, j[0]))
                    i += 1
                myEmail.accounts = readAccounts
                myEmail.selfPassWord = readAccounts['selfPassWord']
                myEmail.users = readAccounts['users']
                myEmail.smtp = readAccounts['smtp']
                myEmail.pop3 = readAccounts['pop3']
                myEmail.tempSelfPassWord = checked[1]
            else:
                print('个人密钥错误，解密失败！')
                readAccounts(myEmail)
        else:
            print('本地数据为空，开始新建账户信息数据库...')
            setAccounts(myEmail)
    else:
        print('本地数据为空，开始新建账户信息数据库...')
        setAccounts(myEmail)


def chooseFunction():
    print('------------------------------------------------------------')
    print('欢迎使用我的邮箱客户端！')
    print('------------------------------------------------------------')
    a = input('发邮件还是收邮件抑或是退出？s/g/e:\n')
    if a == 's':
        sendEmail()
        chooseFunction()
    elif a == 'g':
        getEMail()
        chooseFunction()
    elif a == 'e':
        exit()
    else:
        chooseFunction()


def sendEmail():
    # 新建Email类：
    myEmail = MyEmail()
    # 实例化这个类：
    readAccounts(myEmail)
    i = input('使用哪个邮箱(直接输入前面邮箱的序号即可，如果使用其他账户请不要输入任何数据)？\n')
    if re.match(r'^\d\d*', i):
        user = myEmail.users[int(i)-1]
        print('登陆账户为：%s' % user[0])
        emailName = user[0].split('@')[1]
        try:
            smtp = myEmail.smtp[emailName]
        except:
            print('未能查询到保存的smtp服务器信息，开始新建服务器信息：')
            smtp = input('请按smtp.example.com:port格式输入smtp服务器及端口：')
            m = input('smtp服务器采用SSL加密请按0，STARTTLS加密请按1:')
            myEmail.smtp[emailName] = (
                smtp.split(':')[0], int(smtp.split(':')[1]), m)
            myEmail.updateAccounts()
            with open('pyEmail', 'wb')as f:
                pickle.dump(myEmail.accounts, f)
        print('该账户smtp服务器为：%s:%s' % (smtp[0], smtp[1]))
        addr = user[0]
        passwd = myEmail.decryptData(user[1], myEmail.tempSelfPassWord)
        myEmail.editEmail(addr)
        myEmail.sendEmailBySmtp(addr, passwd, smtp)
    elif i == '':
        print('建立新的账户：')
        print('为保证数据安全，再次验证个人密钥')
        checked = myEmail.checkSelfPassword(myEmail.selfPassWord)
        if checked[0]:
            print('个人密钥验证通过！')
            selfPassWord = checked[1]
            i = input('请输入你要登陆的邮箱地址：')
            j = input('请输入你要登陆的邮箱密码：')
            k = input('请按smtp.example.com:port格式输入smtp服务器及端口：')
            m = input('smtp服务器采用SSL加密请按0，STARTTLS加密请按1:')
            if m == '1':
                m = '1'
            else:
                m == '0'
            l = input('请按pop.example.com:port格式输入pop3服务器及端口：')
            myEmail.users.append(
                (i, myEmail.encipherData(j, selfPassWord)))
            myEmail.smtp[i.split('@')[1]] = (
                k.split(':')[0], int(k.split(':')[1]), m)
            myEmail.pop3[i.split('@')[1]] = (
                l.split(':')[0], int(l.split(':')[1]))
            myEmail.updateAccounts()
            with open('pyEmail', 'wb')as f:
                pickle.dump(myEmail.accounts, f)
            print('新账号设置完毕！')
            chooseFunction()
        else:
            print('个人密钥验证失败，请重试!')
            sendEmail()
    else:
        print('输入非法，请重试！')
        sendEmail()


def getEMail():
    # 新建Email类：
    myEmail = MyEmail()
    # 实例化这个类：
    readAccounts(myEmail)
    i = input('使用哪个邮箱(直接输入前面邮箱的序号即可，如果使用其他账户请不要输入任何数据)？\n')
    if re.match(r'^\d\d*', i):
        user = myEmail.users[int(i)-1]
        print('登陆账户为：%s' % user[0])
        emailName = user[0].split('@')[1]
        try:
            pop3 = myEmail.pop3[emailName]
        except:
            print('未能查询到保存的pop3服务器信息，开始新建服务器信息：')
            pop3 = input('请按pop.example.com:port格式输入pop3服务器及端口：')
            myEmail.pop3[emailName] = (
                pop3.split(':')[0], int(pop3.split(':')[1]))
            myEmail.updateAccounts()
            with open('pyEmail', 'wb')as f:
                pickle.dump(myEmail.accounts, f)
        print('该账户的pop3服务器为：%s:%s' % (pop3[0], pop3[1]))
        # 连接pop3服务器
        server = poplib.POP3_SSL(pop3[0], pop3[1])
        # 打印调试信息
        # server.set_debuglevel(1)
        # 可选：打印POP3服务器欢迎信息
        print(server.getwelcome().decode('utf-8'))
        try:
            server.user(user[0])
            server.pass_(myEmail.decryptData(
                user[1], myEmail.tempSelfPassWord))
            loginStatus = True
        except:
            print('身份认证失败，请重试！')
            loginStatus = False
            chooseFunction()
        finally:
            if loginStatus == True:
                # 可以用stat()函数返回邮件数量及占用空间
                print('邮件数量：%s；占用空间：%s' % (server.stat()))
                mails = server.list()[1]
                print('开始打印收件箱(默认读取近15封邮件):')
                myEmail.mailHeader(len(mails), len(mails) - 15, server)
                a = input('请选择要下载邮件的序号(想要查看的邮件不在上述邮件中？请不输入编号)：')
                if re.match(r'^\d\d*', a):
                    try:
                        lines = server.retr(int(a))[1]
                        msgContent = b'\r\n'.join(lines).decode('utf-8')
                        msg = Parser().parsestr(msgContent)
                        print(
                            '------------------------------------------------------------')
                        print('第%s封邮件读取成功，下面显示邮件内容：' % a)
                        print(
                            '------------------------------------------------------------')
                        myEmail.parseMail(msg)
                        print(
                            '############################################################')
                        print('第%s封邮件打印完毕' % a)
                    except:
                        pass
                else:
                    print('显示所有邮件：')
                    myEmail.mailHeader(len(mails), 0, server)
                if server:
                    server.quit()
            else:
                print('身份认证失败，请重试！')
                chooseFunction()
    elif i == '':
        print('建立新的账户：')
        print('为保证数据安全，再次验证个人密钥')
        checked = myEmail.checkSelfPassword(myEmail.selfPassWord)
        if checked[0]:
            print('个人密钥验证通过！')
            selfPassWord = checked[1]
            i = input('请输入你要登陆的邮箱地址：')
            j = input('请输入你要登陆的邮箱密码：')
            k = input('请按smtp.example.com:port格式输入smtp服务器及端口：')
            m = input('smtp服务器采用SSL加密请按0，STARTTLS加密请按1:')
            if m == '1':
                m = '1'
            else:
                m == '0'
            l = input('请按pop.example.com:port格式输入pop3服务器及端口：')
            myEmail.users.append(
                (i, myEmail.encipherData(j, selfPassWord)))
            myEmail.smtp[i.split('@')[1]] = (
                k.split(':')[0], int(k.split(':')[1]), m)
            myEmail.pop3[i.split('@')[1]] = (
                l.split(':')[0], int(l.split(':')[1]))
            myEmail.updateAccounts()
            with open('pyEmail', 'wb')as f:
                pickle.dump(myEmail.accounts, f)
            print('新账号设置完毕！')
            chooseFunction()
        else:
            print('个人密钥验证失败，请重试!')
            chooseFunction()
    else:
        print('输入非法，请重试！')
        chooseFunction()
chooseFunction()
```
&emsp;&emsp;其实用python来收发邮件都很简单的，因为有现成的模块供我们使用，我们需要注意的就是各个模块的各个方法需要传入的参数以及什么时候用什么方法，尤其是SSL加密协议和STARTTLS加密协议以及email.parse模块来解析邮件需要多多注意！