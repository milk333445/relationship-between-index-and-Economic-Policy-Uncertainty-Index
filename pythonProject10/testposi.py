import jieba
import pandas as pd
df=pd.read_csv('工商時報經濟.csv',encoding='utf-8-sig',dtype=str)
artic_seged=jieba.cut(df,cut_all=False)
stopwordslist=open('stopword.txt',encoding='utf-8-sig')#把stopword引進來
stopwords=stopwordslist
outstr=''
for word in artic_seged:
    if word not in stopwords:
        outstr+=' '
return outstr


