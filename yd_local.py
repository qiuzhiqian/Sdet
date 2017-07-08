#!/usr/bin/env python
# coding = utf-8  

import os
import sqlite3

class Sql_operate():
    def __init__(self):
        db_file=os.path.split(os.path.realpath(__file__))[0]+'/script/wordDB.db'
        # 连接到SQLite数据库
        # 数据库文件是test.db
        # 如果文件不存在，会自动在当前目录创建:
        self.conn = sqlite3.connect(db_file)
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        
        # 执行一条SQL语句，创建Ewordmap表:
        self.cursor.execute('create table if not exists Ewordmap (id varchar(20) primary key,name varchar(20),pronounce1 varchar(10),pronounce2 varchar(10),result1 varchar(40),result2 varchar(40),result3 varchar(40),result4 varchar(40),result5 varchar(40))')
        
        # 执行一条SQL语句，创建Cwordmap表:
        self.cursor.execute('create table if not exists Cwordmap (id varchar(20) primary key,name varchar(20),pronounce1 varchar(10),pronounce2 varchar(10),result1 varchar(40),result2 varchar(40),result3 varchar(40),result4 varchar(40),result5 varchar(40))')
        
            
    def __del__(self):
        self.cursor.close()

        self.conn.commit()

        self.conn.close()
        
    def SetWord(self,type,word,pronounce,result):
        tableName=''
        if(type=='E2C'):
            tableName='Ewordmap'
        else:
            tableName='Cwordmap'
        
        word_f='"'+word+'"'
        pronounce_f=[]
        for index in range(2):
            if(index<len(pronounce)):
                pronounce_f.append('"'+pronounce[index]+'"')
            else:
                pronounce_f.append('null')
                
        result_f=[]
        for index in range(5):
            if(index<len(result)):
                result_f.append('"'+result[index]+'"')
            else:
                result_f.append('null')
        
        sql_cmd=r'insert into %s values (null,%s,%s,%s,%s,%s,%s,%s,%s)' %(tableName,word_f,pronounce_f[0],pronounce_f[1],result_f[0],result_f[1],result_f[2],result_f[3],result_f[4])
        
        # 继续执行一条SQL语句，插入一条记录:
        self.cursor.execute(sql_cmd)

    def GetWord(self,type,word):
        tableName=''
        if(type=='E2C'):
            tableName='Ewordmap'
        else:
            tableName='Cwordmap'
        word_f='"'+word+'"'
            
        sql_cmd=r'select * from %s where name=%s' %(tableName,word_f)
        # 执行查询语句:
        self.cursor.execute(sql_cmd)
        
        # 获得查询结果集:
        values = self.cursor.fetchall()
        #print(values)
        return values


if __name__=='__main__':
    db_obj=Sql_operate()
    #db_obj.SetWord("E2C","word",['p1','p2'],['r1','r2','r3'])
    #db_obj.SetWord("C2E","单词",['p1','p2'],['r1','r2','r3'])
    
    print(db_obj.GetWord("E2C","xx"))
    print(db_obj.GetWord("C2E","单词"))
    

