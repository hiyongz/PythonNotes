#!/usr/bin/python3
#-*-coding:utf-8-*-
# @Time:    2021/11/14 10:26
# @Author:  hiyongz
# @File:    flask_demo.py

from flask import Flask, escape, request, session

app = Flask(__name__)
app.secret_key = "hiyongz"

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/login', methods=['get','post'])
def login():
    res = {
        "methods": request.method,
        "url": request.path,
        "args": request.args,
        "form": request.form
    }

    session["username"] = request.args.get("name")

    return res



if __name__ == '__main__':
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=1234,
    )

    app.run(**config)
