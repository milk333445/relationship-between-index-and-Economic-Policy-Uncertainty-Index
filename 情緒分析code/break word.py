import pandas as pd
import re
import jieba
import jieba.analyse
import numpy as np
jieba.set_dictionary('dict.txt.big.txt')
def seg_article(init_article):#最原始的資料進行斷詞處理
    artic_seged=jieba.cut(init_article,cut_all=False)
    stopwordslist=open('stopword.txt',encoding='utf-8')#把stopword引進來
    stopwords=stopwordslist
    outstr=''
    for word in artic_seged:
        if word not in stopwords:
            outstr += word
            outstr+=' '
    return outstr

def jieblTFIDF(text,n):#情緒分數
    keywordlist=[]
    tages=jieba.analyse.extract_tags(text,topK=n,withWeight=True)

    for i in range(len(tages)):
        eachword=tages[i][0]
        keywordlist.append(eachword)
    return keywordlist
one=[]
def one_hot(dataframe,keyword,words,date):
    df_zeros=np.zeros((len(dataframe),),dtype=int)
    tempdic=pd.DataFrame({'temp':df_zeros},index=date)
    for eachkey in keyword:
        tempdic[eachkey]=0
    OneHot_df=tempdic.drop('temp',axis=1)
    for j in range(len(words)):
        for word in words[j]:
            if word in keyword:
                OneHot_df[word][j] = 1
    OneHot_df.to_csv('OneHot30日.csv',index=1,header=1,encoding='utf_8_sig')


def sentiment(words,positive,negative,date):
    scorelist=[]
    for i in range(len(words)):
        score=0
        for word in words[i]:
            totalWord=len(words[i])
            if word in positive:
                score+=1
            if word in negative:
                score=score-1
        sentimentWeight=score/totalWord
        scorelist.append(sentimentWeight)
    scoreSeries=pd.Series(scorelist,index=date)
    sentiment_df=pd.DataFrame(scoreSeries,index=date,columns=['sentiment'])
    sentiment_df.to_csv('sentiment30日.csv',encoding='utf-8-sig')

def readfile():
    df=pd.read_csv('中時日報30日資料.csv',encoding='utf-8-sig',dtype=str)
    postive = [line.strip() for line in open('NTUSD_positive_unicode.txt', 'r', encoding='utf-8').readlines()]
    negative = [line.strip() for line in open('NTUSD_negative_unicode.txt', 'r', encoding='utf-8').readlines()]
    textstr=''
    textlist=[]
    onelist=[]
    date1=[]
    date_news=[]
    count=[]
    df['date']=pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    for i in range(len(df)):
        if df['date'][i] not in date1:
            date1.append(df['date'][i])
    for i in range(len(date1)):
        df1=df[df['date']==date1[i]]
        df1=df1.reset_index(drop=True)
        originaltext=''
        count1=len(df1)
        count.append(count1)
        for i in range(len(df1)):
            if type(df1['news'][i]) == str:
                date_news2 = df1['news'][i] + ''
                originaltext += date_news2
        date_news.append(originaltext)

    for i in range(len(date_news)):
        pattern = '[a-zA-Z0-9(/)().?:@，!/、\n]+'
        originaltext = re.sub(pattern, '', date_news[i])
        segtext = seg_article(originaltext)
        textstr += segtext
        textlist.append(segtext)
        onelist.append(segtext.split())
    df2=pd.DataFrame({'date':date1,'count': count, 'news': date_news,})
    df2.to_csv('df30日.csv', encoding='utf_8_sig')
    keywordlist = jieblTFIDF(textstr, 40)
    keywordlistone = ''.join(keywordlist)
    sentiment(onelist, postive, negative, date1)
    one_hot(df2,keywordlist,onelist,date1)
    print(keywordlist)
    print(df2)
    print(onelist)
readfile()












