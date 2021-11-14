#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/14 14:53
# @Author:  hiyongz
# @File:    test_pymysql.py

import pymysql  # python 3.x

# import MySQLdb  # python 2.x

db = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="zhy123456",
    db="testdb",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

class TestPyMysql():
    def test_conn(self):
        with db.cursor() as cursor:
            sql = "show databases;"
            cursor.execute(sql)
            print(cursor.fetchall())

    def test_select(self):
        with db.cursor() as cursor:
            sql = "SELECT * FROM student where name=%s;"
            cursor.execute(sql, ["张三"])
            print(cursor.fetchall())