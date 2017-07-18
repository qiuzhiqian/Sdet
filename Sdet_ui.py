#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------
#Author:qiuzhiqian
#Email:xia_mengliang@163.com
#------------------------

import Sdet_core
import tkinter as tk

top = tk.Tk()
top.title("Sdet")                                       #设置UI标题

TopFrame=tk.Frame(top,width=60)                         #用来布局使用
WordEntry=tk.Entry(TopFrame,width=45)                   #创建一个单行文本框
SearchBtn=tk.Button(TopFrame,text="Search",width=15)    #创建一个按钮

ResultLabel=tk.Label(top,text='Nothing',height=15,width=65,bg='#FFFFDD',justify=tk.LEFT)    #创建一个显示标签

def BtnCallback():                                      #按钮触发回调函数
    words=WordEntry.get()                               #获取文本框中的文本
    sdh=Sdet_core.Sdet_handle()
    if(sdh.priority==0):
        res=sdh.GetWordLocalInfo(words)
        if(res<0):          #本地查询无结果
            sdh.GetWordWebInfo(sdh.GetWebString(words))
            sdh.SaveLocalInfo()     #更新数据库
    else:
        sdh.GetWordWebInfo(sdh.GetWebString(words))
    
    out_string=sdh.Result_Formate()
    ResultLabel.configure(text=out_string,anchor=tk.NW)

SearchBtn.configure(command=BtnCallback)        #设置回调函数

WordEntry.grid(row=0,column=0)              #布局
SearchBtn.grid(row=0,column=1)

TopFrame.grid(row=0,column=0)
ResultLabel.grid(row=1,column=0)


# 进入消息循环
top.mainloop()
