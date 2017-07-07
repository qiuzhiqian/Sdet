#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import urllib.request
import sys

class Dict_Yd:
    type=''
    keyword=''
    phonetic=[]
    result=[]

    def __init__(self):
        self.Trans_yd_result=r'<div id="phrsListTab" class="trans-wrapper clearfix">([\s\S]*?)<div id="webTrans" class="trans-wrapper trans-tab">'
        
        self.Keyword_tag=r'<h2 class="wordbook-js">([\s\S]*?)<span class="keyword">([\s\S]*?)</span>([\s\S]*?)<div class="trans-container">'
        
        self.Content_tag=r'<div class="trans-container">([\s\S]*?)<div id="webTrans" class="trans-wrapper trans-tab">'
    
    def GetWebString(self,words):
        if (ord(list(words)[0]) not in range(97,122) and ord(list(words)[0]) not in range(65,90)):  #中转英
            self.type='C2E'
            words=urllib.request.quote(words)
        else:                                                                                       #英转中
            self.type='E2C'
        
        ydurl=r'http://www.youdao.com/w/eng/'+words+'/#keyfrom=dict2.index'
        user_agent=r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        headers = {'User-Agent':user_agent}
        req = urllib.request.Request(ydurl, headers=headers)
        Res = urllib.request.urlopen(req).read().decode('utf-8')
        return Res
    
    def GetWordInfo(self,webString):
        resultString=''
        keywordString=''
        contentString=''
        formate=r'\s?<.*?>'

        self.keyword=''
        self.phonetic=[]
        self.result=[]
        
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
                wordjsList=re.findall(r'<a class="search-js" href=[\s\S]*?</a>',item)
                for index in range(len(wordtypeList)):
                    self.result.append(re.sub(formate,'',wordtypeList[index])+'\t'+re.sub(formate,'',wordjsList[index]))

    def Result_Formate(self):
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

if __name__=='__main__':
    words=''
    
    #print(len(sys.argv))

    if(len(sys.argv)<2):
        words=input("请输入单词:")
    else:
        words=sys.argv[1]

    yds=Dict_Yd()
    YDWebString=yds.GetWebString(words)
    yds.GetWordInfo(YDWebString)
    out_string=yds.Result_Formate()
    print(out_string)
