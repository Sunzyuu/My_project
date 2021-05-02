# -*- coding = utf - 8 -*-
#@Time : 2021/4/22 16:47
#@Author : sunzy
#@File : dbhelper.py

import pymysql
from scrapy.utils.project import get_project_settings

class DBHelper():

    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']


    def connectMysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8')
        return conn


    def connectDatabase(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')
        return conn

        # 创建要使用到的数据库
    def createDatabase(self):
        conn = self.connectMysql()
        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)  #
        cur.close()
        conn.close()

        # 创建数据表
    def createTable(self, sql):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

        # 向数据库中插入数据
    def insert(self, sql, *params):  #
        conn = self.connectDatabase()
        cur = conn.cursor();
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()
        # 数据库更新操作
    def update(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


    def delete(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

class TestDBHelper():
    def __init__(self):
        self.dbHelper = DBHelper()

    def testCreateDatebase(self):
        self.dbHelper.createDatabase()

    def testCreateTable(self):
        sql = "create table wordtable(id int primary key auto_increment,word varchar(50),soundmark varchar(100),url varchar(200),translation varchar(100))"
        self.dbHelper.createTable(sql)

    def testInsert(self):
        sql = "insert into wordtable(word,soundmark,url,translation) values(%s,%s,%s,%s)"
        params = ("test", "test", "test", "test")
        self.dbHelper.insert(sql, *params)

    def testUpdate(self):
        sql = "update testtable set word=%s,soundmark=%s,url=%s,translation=%s where id=%s"
        params = ("update", "update", "update", "update","1")
        self.dbHelper.update(sql, *params)

    def testDelete(self):
        sql = "delete from wordtable where id=%s"
        params = ("1")
        self.dbHelper.delete(sql, *params)

if __name__ == "__main__":
    testDBHelper = TestDBHelper()
    # testDBHelper.testCreateDatebase()
    # testDBHelper.testCreateTable()
    testDBHelper.testInsert()