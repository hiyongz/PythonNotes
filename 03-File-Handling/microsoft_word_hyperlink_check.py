#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/11 14:16
# @Author:  haiyong
# @File:    microsoft_word_hyperlink_check.py

#settings
import os
import win32com.client
debug = True

# Open a specified word document
wordapp = win32com.client.Dispatch('Word.Application')
wordapp.Visible = debug
wordapp.DisplayAlerts = False		# 关闭警告
wordapp.Visible = True			# 程序可见

directory = os.path.dirname(__file__)
filename = 'word-file-demo.docx'
document_location = os.path.join(directory, filename)

if debug == True:
    print(document_location)

document = wordapp.Documents.Open(document_location)

if debug == True:
    print("Document opened succesfully.")

# Gimme the links
# wordapp.ActiveDocument

for link in (wordapp.ActiveDocument.HyperLinks):
    print("Name: ",link.Name)
    print("Address: ",link.Address)

    # opened_doc = wordapp.Documents(os.path.basename(link.Address))
    # opened_doc.Close()

    try:
        link.Follow(NewWindow=True)
    except:
        print("This link is broken.")
    else:
        print("This link did not raise an error.")








