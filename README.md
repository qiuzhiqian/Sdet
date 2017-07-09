# Sdet 

**S**imple **D**ictionary **E**xpanded **T**ool

这是一个简单的词典拓展工具，界面清新，操作简单，功能精巧。

## 使用平台：
* Windowns
* Linux
* Mac OS

这是一个基于有道词典设计的一个翻译工具。
你可以仅仅在命令行下来使用它，同时它也支持GUI版。
如果是在命令行下使用它，请运行Sdet_core.py。
如果是使用GUI，请运行Sdet_ui.py。
当然Sdet_core.py也可以当作一个模块被其他的py文件调用^_^。
本软件既支持网络搜索，同时也支持本地搜索，而且本软件还集成了一个本地搜索数据库制作的脚本。

## 使用介绍:

* 安装python3.x
* 本地数据库生成
* 软件运行机制
* 命令行无参数
* 命令行带参数
* GUI模式
* 汉译英

### 安装python3.x

略

### 本地数据库生成

本软件默认自带一个含有2000基本词汇的本地数据库，该数据库位于{rootdir}/script/Sdet_wordDB.db

如果本软件运行时，该数据库文件不存在，那么软件会自动创建一个空的数据库。如果本地数据库损毁，本软件提供一下方法恢复基本的数据库：
方法一：从软件下载的地方重新下载一份DB文件，放置到script下
方法二：用本软件自带的DB制作脚本重新制作一份含基本单词的DB文件
1. 将需要导入数据库的单词添加到数据库生成索引文件中，每一行表示一个单词，一行只需要有一个单词即可，其他的行号、注释的都是无效的文本，会自动忽略
2. 不要有空白行
3. 运行脚本Sdet_dbMaker.py，然后等待数据库制作完成，如果索引量比较大的话，数据库生成可能比较慢，这也跟网络有关
![](https://raw.githubusercontent.com/qiuzhiqian/yd_dict/master/doc/1.png)

### 软件运行机制

本软件运行后会请求一个查询单词，支持英文和中文查询，软件首先会在本地数据库中进行搜索本单词的解释，如果本地数据库中有本单词的解释，则直接使用这个解释。如果本地数据库中无该单词的解释，本软件会从网络获取解释，获取成功后该解释会自动写入本地数据库，以供下次搜索是能直接从本地数据库中搜索。

### 命令行无参数

命令行无参数时，软件会提示输入查询的单词

![](https://raw.githubusercontent.com/qiuzhiqian/yd_dict/master/doc/2.png)

### 命令行带参数

命令行带参数时，参数即为查询的单词

![](https://raw.githubusercontent.com/qiuzhiqian/yd_dict/master/doc/3.png)

## GUI模式

直接运行main_ui.py进入GUI模式，在文本框中输入单词，点击搜索即可查询翻译

![](https://raw.githubusercontent.com/qiuzhiqian/yd_dict/master/doc/4.png)

## 汉译英

本词典支持汉译英和英译汉，前面的实例是英译汉的，下面演示汉译英

![](https://raw.githubusercontent.com/qiuzhiqian/yd_dict/master/doc/5.png)

![](https://raw.githubusercontent.com/qiuzhiqian/yd_dict/master/doc/6.png)

如果你觉得我的软件对你有帮助，那就捐助我吧：

![](http://osrkwmsng.bkt.clouddn.com/Alipay.jpg)
