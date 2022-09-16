import requests as rq
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
from pandas.tests.io.json.conftest import orient

user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

title=[]
body=[]
publish_time=[]
page1=input('data-page=')
page1=int(page1)
keyword='經濟'
for page in range(1,page1+1):
    headers = {

        'user-agent': random.choice(user_agents)

    }
    print('start collecting ctee page {page}'.format(page=page))
    home_url='https://www.chinatimes.com/search/{}?page={}'.format(keyword,page)
    r = rq.get(home_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')


    for i in range(0,len(soup.select('div.col'))):
        url=soup.select('div.col')[i].select('a')[0]['href']
        r_content = rq.get(url, headers=headers)
        soup_content = BeautifulSoup(r_content.text, 'lxml')
        title.append(soup_content.find('h1', attrs={'class':'article-title'}).text)
        body.append(''.join(str(x) for x in soup_content.select('div.article-body p')))
        publish_time.append(soup_content.find('span','date').text)
        print(soup_content.find('h1', attrs={'class':'article-title'}).text)
        time.sleep(1)

data=pd.DataFrame({
    'date':publish_time,
    'title':title,
    'news':body
},index=publish_time)
df_reset=data.set_index('date')
df_reset.to_csv('中時日報30日資料.csv',encoding='utf-8-sig')

