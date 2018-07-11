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
    sql = """INSERT INTO runoob_tbl(runoob_title, runoob_author, submission_date)VALUES("学习 PHP", "菜鸟教程", NOW());"""
    conn.executeSQL(sql=sql)
