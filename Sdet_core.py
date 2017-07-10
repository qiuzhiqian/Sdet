#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------
#Author:qiuzhiqian
#Email:xia_mengliang@163.com
#------------------------

import re
import time
import urllib.request
import sys

import Sdet_local

class Sdet_handle:
    banner=r"""
 ____        __          __      
/\  _`\     /\ \        /\ \__   
\ \,\L\_\   \_\ \     __\ \ ,_\  
 \/_\__ \   /'_` \  /'__`\ \ \/  
   /\ \L\ \/\ \L\ \/\  __/\ \ \_ 
   \ `\____\ \___,_\ \____\\ \__\
    \/_____/\/__,_ /\/____/ \/__/"""
    
    version='1.0.0'
    
    priority=0      #搜索优先级,=0先本地搜索，本地失败然后网络搜索,=1不进行本地搜索，直接网络搜索
    
    type=''
    keyword=''
    phonetic=[]
    result=[]

    def __init__(self):
        self.Trans_yd_result=r'<div id="phrsListTab" class="trans-wrapper clearfix">([\s\S]*?)<div id="webTrans" class="trans-wrapper trans-tab">'
        
        self.Keyword_tag=r'<h2 class="wordbook-js">([\s\S]*?)<span class="keyword">([\s\S]*?)</span>([\s\S]*?)<div class="trans-container">'
        
        self.Content_tag=r'<div class="trans-container">([\s\S]*?)<div id="webTrans" class="trans-wrapper trans-tab">'
        
        self.db_obj=Sdet_local.Sql_operate()       #链接数据库
    
    def GetWebString(self,words):
        if (ord(list(words)[0]) not in range(97,122) and ord(list(words)[0]) not in range(65,90)):  #中转英
            self.type='C2E'
            words=urllib.request.quote(words)
        else:                                                                                       #英转中
            self.type='E2C'
        
        ydurl=r'http://www.youdao.com/w/eng/'+words+'/#keyfrom=dict2.index'
        user_agent=r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        headers = {'User-Agent':user_agent}
        try:
            req = urllib.request.Request(ydurl, headers=headers)
            Res = urllib.request.urlopen(req).read().decode('utf-8')
            return Res
        except:
            return ''
        
    
    def GetWordWebInfo(self,webString):
        resultString=''
        keywordString=''
        contentString=''
        formate=r'\s?<.*?>'

        self.keyword=''
        self.phonetic=[]
        self.result=[]
        
        if(webString==''):       #无法获取网页内容(网络有问题)
            return
        
        resultString=re.search(self.Trans_yd_result,webString).group(0)
        keywordString=re.search(self.Keyword_tag,resultString).group(0)

        dcString=re.search(r'<span class="keyword">.*?</span>',keywordString)
        self.keyword=re.sub(formate,'',dcString[0])

        EybStringList=re.findall(r'<span class="phonetic">.*?</span>',keywordString)
        for item in EybStringList:
            self.phonetic.append(re.sub(formate,'',item))

        contentString=re.search(self.Content_tag,resultString).group(0)

        if(self.type=='E2C'):                                               #获取英转中解释列表
            jsStringList=re.findall(r'<li>.*?</li>',contentString)
            for item in jsStringList:
                self.result.append(re.sub(formate,'',item))
            
        elif(self.type=='C2E'):                                             #获取中转英解释列表
            jsStringList=re.findall(r'<p class="wordGroup">[\s\S]*?</span>\s*?</p>',contentString)
            for item in jsStringList:
                wordtypeList=re.findall(r'<span style="font-weight[\s\S]*?</span>',item)
                wordtypeLen=len(wordtypeList)
                wordjsList=re.findall(r'<a class="search-js" href=[\s\S]*?</a>',item)
                for index in range(len(wordjsList)):
                    if(index<wordtypeLen):
                        self.result.append(re.sub(formate,'',wordtypeList[index])+'\t'+re.sub(formate,'',wordjsList[index]))
                    else:
                        self.result.append(re.sub(formate,'',wordjsList[index]))

    def GetWordLocalInfo(self,words):
        self.type=''
        self.keyword=''
        self.phonetic=[]
        self.result=[]
        
        if (ord(list(words)[0]) not in range(97,122) and ord(list(words)[0]) not in range(65,90)):  #中转英
            self.type='C2E'
            words=urllib.request.quote(words)
        else:                                                                                       #英转中
            self.type='E2C'
        
        word_list=self.db_obj.GetWord(self.type,words)            #数据库查询
        
        if(word_list==[]):
            return -1
            
        word_result=word_list[0]
        
        self.keyword=word_result[1]
        
        for index in range(2):
            if(word_result[2+index]!=None):
                self.phonetic.append(word_result[2+index])
            else:
                break
                
        for index in range(5):
            if(word_result[4+index]!=None):
                self.result.append(word_result[4+index])
            else:
                break
                
        return 0
        
    def SaveLocalInfo(self):
        self.db_obj.SetWord(self.type,self.keyword,self.phonetic,self.result)
                    
    def Result_Formate(self):
        if(self.keyword=='' or self.result==[]):        #网络有问题或者单词无有效解释
            return 'Search Error'
        f_string="%s\n" %(self.keyword)
        if(len(self.phonetic)==2 and self.type=='E2C'):
            f_string=f_string+("英:%s\t美:%s" %(self.phonetic[0],self.phonetic[1]))
        elif(len(self.phonetic)==1 and self.type=='C2E'):
            f_string=f_string+("拼音:%s" %(self.phonetic[0]))

        if(len(self.result)):
            f_string=f_string+"\n解释:\n"
            for index in range(len(self.result)):
                f_string=f_string+("\t%d: %s\n" %(index+1,self.result[index]))
        return f_string
        
    def DB_Reset(self,nums):                 #数据库恢复
        self.db_obj.DBReset(nums)

def main():
    words=''

    sdh=Sdet_handle()
    
    if(len(sys.argv)<2):
        words=input("请输入单词:")
    elif(sys.argv[1]=='-h' or sys.argv[1]=='--help' or sys.argv[1]=='-v' or sys.argv[1]=='--version' ):
        print(sdh.banner)
        print("\nversion:%s" %sdh.version)
        return
    else:
        words=sys.argv[1]
    
    if(sdh.priority==0):
        res=sdh.GetWordLocalInfo(words)
        if(res<0):          #本地查询无结果
            sdh.GetWordWebInfo(sdh.GetWebString(words))
            sdh.SaveLocalInfo()     #更新数据库
            #print("******搜索结果来自网络******")
        #else:
            #print("******搜索结果来自本地******")
    else:
        sdh.GetWordWebInfo(sdh.GetWebString(words))
        #print("******搜索结果来自网络******")
    
    out_string=sdh.Result_Formate()
    print(out_string)

if __name__=='__main__':
    main()
