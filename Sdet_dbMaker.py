#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------
#Author:qiuzhiqian
#Email:xia_mengliang@163.com
#------------------------

import re
import os

import Sdet_core

sdh=Sdet_core.Sdet_handle()

db_file=os.path.split(os.path.realpath(__file__))[0]+'/script/Sdet_dbIndex.txt'
file_obj=open(db_file,mode='r',encoding='UTF-8')
fileLine=file_obj.readlines()

reg_cmd=r'[a-zA-Z]+'

lineLen=len(fileLine)
for index in range(lineLen):
    #print(line)
    words=re.search(reg_cmd,fileLine[index]).group(0)
    
    res=sdh.GetWordLocalInfo(words)
    if(res<0):          #本地查询无结果
        print("[%d/%d]:%s" %(index,lineLen,words))
        sdh.GetWordWebInfo(sdh.GetWebString(words))
        sdh.SaveLocalInfo()     #更新数据库

