#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 每日图片api '

__author__ = 'fslong'
__version__ = '0.0.1'

import asyncio
import base64
import json
import os
import re
import traceback, pymysql, datetime
import asyncio


class MySQLConnection(object):
    # 先声明默认的连接所需变量；
    def __init__(
            self,
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='passwd',
            dbName='TESTDB',
            tabName='testTable',
            dictData={
                'id': 1,
                'test1': 'test',
                'test2': 1.1,
                'test3': b'test',
                'test4': datetime.datetime(2018, 8, 7)
            }):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.tabName = tabName
        self.dictData = dictData

    # 创建数据表的函数：
    def createTable(self, dictData={}):
        if dictData == {}:
            dictData = self.dictData
        sql = """CREATE TABLE IF NOT EXISTS `%s`(""" % self.tabName
        keys = []
        for i in dictData:
            keys.append(i)
        for i in range(len(keys)):
            if i == 0:
                sql += """%s VARCHAR(40) , """ % keys[i]
            else:
                if isinstance(dictData[keys[i]], int):
                    sql += """%s INT , """ % keys[i]
                elif isinstance(dictData[keys[i]], float):
                    sql += """%s FLOAT(20,4) , """ % keys[i]
                elif isinstance(dictData[keys[i]], datetime.datetime):
                    sql += """%s DATETIME , """ % keys[i]
                elif isinstance(dictData[keys[i]], (bytes, bytearray)):
                    sql += """%s BLOB , """ % keys[i]
                else:
                    sql += """%s TEXT , """ % keys[i]
        sql += """PRIMARY KEY (`%s`))ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % keys[
            0]
        #print(sql)
        self.executeSQL(sql)

    # 执行提交sql语句的函数：
    def executeSQL(self, sql):
        db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.dbName,
            use_unicode=True,
            charset='utf8')
        cursor = db.cursor()
        # 使用execute()驱动数据库并执行语句：
        try:
            if sql.startswith('SELECT'):
                cursor.execute(sql)
                results = cursor.fetchall()
            else:
                results = cursor.execute(sql)
                # 提交到数据库执行：
                db.commit()
                # 获取所有记录列表
        except:
            traceback.print_exc()
            results = '奇怪的MySq语句！'
            # 如果发生错误则回滚：
            db.rollback()
        # 关闭数据库链接：
        db.close
        return results

    # 插入数据的函数：
    def insertData(self, dictData={}):
        if dictData != {}:
            self.dictData = dictData
        else:
            print('没有输入要存储的数据呀！')
            #return None
        # 先看下表结构有没有生成，没有生成就生成一下:
        #self.executeSQL()
        # 拼接sql语句：
        sql = """INSERT INTO %s (""" % (self.tabName, )
        for i in self.dictData:
            sql += """%s,""" % i
        sql = sql[0:-1] + """)""" + """VALUES("""
        for i in self.dictData:
            if isinstance(self.dictData[i], (int, float)):
                string = self.dictData[i]
            else:
                string = '\"' + str(self.dictData[i]) + '\"'
            sql += """%s,""" % string
        sql = sql[0:-1] + """);"""
        results = self.executeSQL(sql)
        return results

    # 删除数据库内容的函数：
    def deleteData(self, column, data):
        sql = """DELETE FROM %s WHERE %s=%s;""" % (self.tabName, column, data)
        results = self.executeSQL(sql)
        return results

    # 更新数据库内容的函数:
    def updateData(self, column1, data1, column2, data2):
        sql = """UPDATE %s SET %s = %s WHERE %s = %s""" % (self.tabName,
                                                           column2, data2,
                                                           column1, data1)
        results = self.executeSQL(sql)
        return results

    # 查找数据库的函数：
    def selectData(self, column='', data=''):
        if column == '':
            sql = """SELECT * FROM %s;""" % self.tabName
        else:
            sql = """SELECT * FROM %s WHERE %s='%s';""" % (self.tabName,
                                                           column, data)
        results = self.executeSQL(sql)
        return results


def wallpaper(picType=0, num=1, transfer=0):
    pics = []
    types = ('pc', 'mobile', 'girls')
    allData = (39664, 10088, 5271)
    '''# 暂时先可以提供负值
    if picType < 0:
        picType = 0
    if num < 0:
        num = 1
    if transfer < 0:
        transfer = 0
    '''
    for i in range(num):
        date = datetime.datetime.now()
        date0 = datetime.datetime(2000, 1, 1)
        dayTransfer = int((date - date0).days) - i - transfer
        dayTransfer = dayTransfer % allData[picType % 3]
        if dayTransfer > 0:
            try:
                mysql = MySQLConnection(
                    dbName='WALLPAPER', tabName=types[picType % 3])
                pic = mysql.selectData(column='picId', data=dayTransfer)[0]
                if pic != () and pic != '()':
                    pics.append({
                        'picId': pic[0],
                        'picName': pic[1],
                        'picIntro': pic[2],
                        'picSize': pic[3],
                        'picUrl': pic[4],
                        'picPre': pic[5],
                        'picColumn': pic[6],
                        'picTag': pic[7],
                        'picNum': pic[8],
                        'picType': pic[9],
                    })
            except:
                pics.append('erro')
    return pics


if __name__ == '__main__':
    mysql = MySQLConnection(dbName='WALLPAPER', tabName='wallpaper')
    picsPC = mysql.selectData(column='picType', data='电脑壁纸')
    picsMobile = mysql.selectData(column='picType', data='手机壁纸')
    picsGirls = mysql.selectData(column='picType', data='美女图片')
    i = 0
    for pic in picsGirls:
        i += 1
        picDict = {
            'picId': i,
            'picName': pic[1],
            'picIntro': pic[2],
            'picSize': pic[3],
            'picUrl': pic[4],
            'picPreview': pic[5],
            'picColumn': pic[6],
            'picTag': pic[7],
            'picNum': pic[8],
            'picType': pic[9],
        }
        mysql.tabName = 'girls'
        mysql.insertData(picDict)