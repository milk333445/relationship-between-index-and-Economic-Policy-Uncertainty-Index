import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random

while True:

    try:
        pages_input = int(input("請問要抓取八卦版幾頁的文章?\n請輸入頁數："))
        break
    except:
        print("請輸入天數（數字）！")
URL = "https://www.ptt.cc/bbs/Gossiping/index.html"
my_headers = {'cookie': 'over18=1;',
              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
last_page_list=[]
response = requests.get(URL, headers = my_headers)
soup = BeautifulSoup(response.text,"html5lib")
latest_urls = soup.select("a[class='btn wide']")
for url in latest_urls:
    last_page_list.append(url['href'])
latest_url=last_page_list[1]
last_page_num=int(''.join([x for x in latest_url if x.isdigit()]))
pageNum = last_page_num
print(pageNum)
df = pd.DataFrame()  #暫存當頁資料，換頁時即整併到dfAll
dfAll= pd.DataFrame()


for i in range(pages_input):
    my_headers = {'cookie': 'over18=1;',
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
    nexturl = "https://www.ptt.cc/bbs/Gossiping/index" + str(pageNum) + ".html"
    for i in range(pages_input):
        # 設定Header與Cookie
        my_headers = {'cookie': 'over18=1;'}

    nexturl = "https://www.ptt.cc/bbs/Gossiping/index" + str(pageNum) + ".html"
    if i == 0:
        print(f'getting data from: {URL}')
        response = requests.get(URL, headers=my_headers)
    else:
        response = requests.get(nexturl, headers=my_headers)
        print(f'抓取頁面資料中: {nexturl}')

    web_content = response.text
    soup = BeautifulSoup(web_content, "html5lib")
    rents = soup.find_all("div", "r-ent")
    titles = [r.find('div', "title").text.strip() for r in rents]

    links = []
    for l in rents:
        try:
            temp_url = l.find('a')['href']
            link = "https://www.ptt.cc" + temp_url
            # print(link)
            links.append(link)

        except:
            links.append("")

    dates = [d.find('div', "meta").find("div", "date").text.strip() for d in rents]
    counts = [c.find('div', "nrec").text.strip() for c in rents]

    df = pd.DataFrame(
        {
            '標題': titles,
            '連結': links,
            "日期": dates,
            "推文數": counts
        })

    dfAll = pd.concat([df, dfAll])
    dfAll = dfAll.reset_index(drop=True)

    pageNum -= 1
print(dfAll)
rows=dfAll.shape[0]
article = []
for i in range(rows):
    my_headers = {'cookie': 'over18=1;'}
    # 這邊為了簡化就沒用隨機user-agent了

    target_url = dfAll.loc[:, "連結"][i]

    try:
        print(f"正處理第{i}個網址：{target_url}")
        r = requests.get(target_url, headers=my_headers)
        web_content = r.text
        # print(web_content)
        soup = BeautifulSoup(web_content, 'html5lib')

        articleContent = soup.select("#main-content")

        for p in articleContent:
            article.append(p.text.strip().replace("\n", ""))

    except:
        continue
df=pd.DataFrame(article)
df.to_csv('article.csv',encoding='utf-8-sig')
df2=pd.DataFrame(dfAll)
df2.to_csv('news.csv',encoding='utf-8-sig')