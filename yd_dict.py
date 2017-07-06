#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import urllib.request
import sys

class Dict_Yd:
    keyword=''
    phonetic=[]
    result=[]
	
    def __init__(self):
        self.Trans_yd_result=r'<div id="phrsListTab" class="trans-wrapper clearfix">([\s\S]*?)<div id="webTrans" class="trans-wrapper trans-tab">'
        
        self.Keyword_tag=r'<h2 class="wordbook-js">([\s\S]*?)<span class="keyword">([\s\S]*?)</span>([\s\S]*?)<div class="trans-container">'
        
        self.Content_tag=r'<div class="trans-container">([\s\S]*?)<div id="webTrans" class="trans-wrapper trans-tab">'
    	
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
        #print(self.keyword)

        EybStringList=re.findall(r'<span class="phonetic">.*?</span>',keywordString)
        for item in EybStringList:
            self.phonetic.append(re.sub(formate,'',item))

        contentString=re.search(self.Content_tag,resultString).group(0)

        jsStringList=re.findall(r'<li>.*?</li>',contentString)
        for item in jsStringList:
            self.result.append(re.sub(formate,'',item))
    	
    def GetWebString(self,words):
        ydurl=r'http://www.youdao.com/w/eng/'+words+'/#keyfrom=dict2.index'
        user_agent=r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        headers = {'User-Agent':user_agent}
        req = urllib.request.Request(ydurl, headers=headers)
        Res = urllib.request.urlopen(req).read().decode('utf-8')
        return Res

    def Result_Formate(self):
        f_string="%s\n" %(self.keyword)
        if(len(self.phonetic)==2):
            f_string=f_string+("英:%s\t美:%s" %(self.phonetic[0],self.phonetic[1]))

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
