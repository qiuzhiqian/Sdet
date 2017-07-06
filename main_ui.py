#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import yd_dict
import tkinter as tk

top = tk.Tk()
top.title("YDDict")

TopFrame=tk.Frame(top,width=60)
WordEntry=tk.Entry(TopFrame,width=45)
SearchBtn=tk.Button(TopFrame,text="Search",width=15)

ResultLabel=tk.Label(top,text='Nothing',height=15,width=65,bg='#FFFFDD',justify=tk.LEFT)

def BtnCallback():
    words=WordEntry.get()
    YD_Dict=yd_dict.Dict_Yd()
    YD_Dict.GetWordInfo(YD_Dict.GetWebString(words))
    out_string=YD_Dict.Result_Formate()
    ResultLabel.configure(text=out_string,anchor=tk.NW)

SearchBtn.configure(command=BtnCallback)

WordEntry.grid(row=0,column=0)
SearchBtn.grid(row=0,column=1)

TopFrame.grid(row=0,column=0)
ResultLabel.grid(row=1,column=0)


# 进入消息循环
top.mainloop()
