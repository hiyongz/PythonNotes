#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/14 15:23
# @Author:  hiyongz
# @File:    test_sqlalchemy.py

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = "localhost"
port = 3306
user = "root"
password = "zhy123456"
db = "testdb"
charset = "utf8mb4"

Base = declarative_base()


class User(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sex = Column(String)
    age = Column(Integer)
    dept = Column(String)


def test_orm():

    print(password)
    engine = create_engine(
        'mysql+pymysql://{user}:{password}@{host}/{db}'.format(
            user=user, password=password, host=host, db=db),
        echo=True
    )
    # engine = create_engine(
    #     'mysql+pymysql://{user}:{password}@{host}/{db}'.format(user,password, host,db), echo=True
    # )
    Session = sessionmaker(bind=engine)
    session = Session()

    # 插入一条记录
    u1 = User(
        name="小王",
        sex="男",
        age=28,
        dept="通信"
    )

    session.add(u1)
    session.commit()
    u2 = session.query(User).filter_by(name="小王").first()
    print(u2.name)
    assert u2.name == u1.name
