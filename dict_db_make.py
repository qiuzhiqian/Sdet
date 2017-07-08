#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

import yd_dict

YD_Dict=yd_dict.Dict_Yd()

db_file=os.path.split(os.path.realpath(__file__))[0]+'\\script\\make_script.txt'
file_obj=open(db_file,mode='r',encoding='UTF-8')
fileLine=file_obj.readlines()

reg_cmd=r'[a-zA-Z]+'

lineLen=len(fileLine)
for index in range(lineLen):
    #print(line)
    words=re.search(reg_cmd,fileLine[index]).group(0)
    
    res=YD_Dict.GetWordLocalInfo(words)
    if(res<0):          #本地查询无结果
        print("[%d/%d]:%s" %(index,lineLen,words))
        YDWebString=YD_Dict.GetWebString(words)
        YD_Dict.GetWordWebInfo(YDWebString)
        YD_Dict.SaveLocalInfo()     #更新数据库

