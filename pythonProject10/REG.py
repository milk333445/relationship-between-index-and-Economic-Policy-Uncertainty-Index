# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:09:07 2021

@author: Shawn
"""
#re 練習場
#https://regex101.com/
import re
import os
import pandas as pd
os.getcwd()
os.chdir("C:\\Users\\User\\Desktop\\NLP")

f = open('martin-luther-king-i-have-a-dream-speech.txt')
Martin = f.read()

file = "un-general-debates-blueprint.csv"
df = pd.read_csv(file)
YahooNews=pd.read_csv('研究報告—個股09-12_utf8.csv')

pattern = r"Cookie"
sequence = "Cookie"
re.match(pattern, sequence)

pattern = r"dream"
sequence="dreams are very important"
re.match(pattern,sequence)
#Python 提供了两种不同的操作：基于 re.match() 检查字符串开头，或者 re.search() 检查字符串的任意位置（默认Perl中的行为）。
#match 只會找字串裡的開頭
re.match(pattern,'I have a dream')


pattern=r'I have a dream'
#找到的第一個東西的位置
re.search(pattern,Martin)
#把找到的第一個東西列出來
re.search(pattern,Martin).group()
#把找到的所有東西列出來
re.findall(pattern,Martin)

re.findall(r'United Nations',df['text'][1])
re.findall(r'外資',YahooNews['Context'][0])
#寫法2 先把外資變成RE存起來
r1=re.compile(r'外資')
r1.findall(YahooNews['Context'][0])
#將dream 換成 illusion
re.sub(r'dream',r'illusion',Martin)
#依照換成將文字切開
M1 = re.split(r'\n',Martin)

### .
print(Martin)
Martin #print with \n

re.search(r'Co.k.e', 'Cookie').group()
#英文字後面加.代表單複數都要
re.search(r'truth.',Martin)
re.search(r'truth.',Martin).group()
re.findall(r'ha..',Martin)
#兩個點代表前兩個
#.代表任何字元除了換行符號
#[.]就會變成代表句號
re.findall(r'..I',Martin)
#[', I', '. I', 't I', 'e I']
re.findall(r'...I',Martin)
#['w, I', 'n. I', 'at I', 'ee I']

re.findall(r'外.',YahooNews['Title'][1])


re.search(r'^Eat', "Eat cake!").group()
re.search(r'cake$', "Cake! Let's eat cake").group()
re.search(r'^美中',YahooNews['Context'][1]).group()
re.search(r'不變。 $',YahooNews['Context'][1]).group()

#在正規表示法用中括號表示，在這集合內的東西都可以
#ex:現在是過去式都可以
re.findall(r'r[ua]n','run and ran')
#[0-9]0-9數字都可以 [a-z]a到z都可以
#ex:re.findall(r'covid-[0-9][0-9]','covid-19,but covid-20')
#Out:['covid-19', 'covid-20']
#re.findall(r'covid-[0-9]','covid-19,but covid-20')
#Out: ['covid-1', 'covid-2']

ex1='1. A small sentence -2. Another tiny sentence. 3 A smart description'
re.findall(r'sm[a-z][a-z][.a-z0-9]',ex1 )
#Out[27]: ['small', 'smart']
#[^l] 不要l
re.findall(r'sm[a-z][^l][.a-z0-9]',ex1 )
#Out[28]: ['smart']
#\d	匹配一个数字字符。等价于 [0-9]。
#在特殊符號前面加上\會逃脫功能
#原本.代表任意字符，\.則代表一點
# +, *, ., |, (), $,{} 在中括號裡面has no special meaning
re.findall(r'\d\.',ex1 )

re.search(r'[0-9]', 'Number: 5')
re.search(r'[0-9]', 'Number: 5').group()

re.search(r'Number: [^5]', 'Number: 0').group()

#re.search(r'Number: [^5]', 'Number: 5').group()



#\s 匹配任何空白字符，包括空格、制表符、换页符等等。等价于 [ \f\n\r\t\v]。
re.findall(r'Not a\sregular character', 'Not a regular character')
#若在\前面加一個\ ，\\s 則無特殊意義
re.findall(r'Not a \\sregular character', 'Not a \sregular character')
#Out[33]: ['Not a \\sregular character']
re.search(r'Not a\sregular character', 'Not a regular character').group()
re.search(r'Just a \regular character', 'Just a \regular character').group()
re.search(r'Just a \\sregular character', 'Just a \sregular character').group()

#\w匹配包括下划线的任何单词字符。等价于'[A-Za-z0-9_]'。
print("Lowercase w:", re.search(r'Co\wk\we', 'Cookie').group())
#\W	匹配任何非单词字符。等价于 '[^A-Za-z0-9_]'。
print("Uppercase W:", re.search(r'C\Wke', 'C@ke').group())

print("Uppercase W won't match, and return:", re.search(r'Co\Wk\We', 'Cookie'))

print("Lowercase s:", re.search(r'Eat\scake', 'Eat cake').group())
print("Uppercase S:", re.search(r'cook\Se', "Let's eat cookie").group())


print("How many cookies do you want? ", re.search(r'\d+', '100 cookies').group())


re.search(r'Co+kie', 'Cooookie').group()

re.search(r'Ca*o*kie', 'Cookie').group()


re.search(r'Colou?r', 'Color').group()


re.search(r'\d{9,10}', '0987654321').group()

statement = 'Please contact us at: support@datacamp.com'
match = re.search(r'([\w\.-]+)@([\w\.-]+)', statement)
if statement:
  print("Email address:", match.group()) # The whole matched text
  print("Username:", match.group(1)) # The username (group 1)
  print("Host:", match.group(2)) # The host (group 2)

##<>
statement = 'Please contact us at: support@datacamp.com'
#()可用來grouping
match = re.search(r'(?P<email>(?P<username>[\w\.-]+)@(?P<host>[\w\.-]+))', statement)
if statement:
  print("Email address:", match.group('email'))
  print("Username:", match.group('username'))
  print("Host:", match.group('host'))

raw_data = "555-1239Moe Szyslak(636) 555-0113Burns, C. Montgomery555-6542Rev. Timothy Lovejoy555 8904Ned Flanders636-555-3226Simpson, Homer5553642Dr. Julius Hibbert"
phone=re.findall(r'[\d,-]{7,11}', raw_data)
name=re.findall(r'[a-zA-Z]+[/s.a-z A-z]*',  raw_data)
#\d{1,2} 一位數或兩位數
re.findall(r'\d{1,2}月', YahooNews['Context'][0])
#找尋股價點數
#[\u4E00-\u9FFF] 所有中文字符
#re+	匹配1个或多个的表达式。
#re*	匹配0个或多个的表达式。
#re{ n, m}	匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式
#re?	匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式
#re{ n}	精确匹配 n 个前面表达式。例如， o{2} 不能匹配 "Bob" 中的 "o"，但是能匹配 "food" 中的两个 o。
#re{ n,}	匹配 n 个前面表达式。例如， o{2,} 不能匹配"Bob"中的"o"，但能匹配 "foooood"中的所有 o。"o{1,}" 等价于 "o+"。"o{0,}" 则等价于 "o*"。
re.findall(r'\d{1,5}\,\d{1,5}點', YahooNews['Context'][0])
re.findall(r'[,\d]+點', YahooNews['Context'][0])
re.findall(r'\d+\,\d+點', YahooNews['Context'][0])
re.findall(r'\d*\,\d*點', YahooNews['Context'][0])
# ['11,270點', '11,270點', '13,221點']

photoTD='1. sh123456, 2 . 123456,3 .sd456565'
#抓取身分證碼
re.findall(r'[\w]+[\d]', photoTD)
re.findall(r'[\w*]+[\d*]', photoTD)
