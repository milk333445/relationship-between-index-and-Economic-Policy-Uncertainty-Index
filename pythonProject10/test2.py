from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import time
import pandas as pd
import random
browser = webdriver.Chrome()
browser.get("https://www.ettoday.net/news/news-list-2022-08-28-17.htm")
one_day_ago = datetime.now() - timedelta(days =1)
one_day_ago_time = one_day_ago.strftime("%Y/%m/%d %H:%M")
print("一天前時間：", one_day_ago_time)
last_height = browser.execute_script("return document.body.scrollHeight")
go=True

while go:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, "lxml")

    new_height = browser.execute_script("return document.body.scrollHeight")

    #已經到頁面底部
    if new_height == last_height:
        print("已經到頁面最底部，程序停止")
        break

    last_height = new_height

    for d in soup.find(class_="part_list_2").find_all('h3'):
        #已經超出兩小時
        if datetime.strptime(d.find(class_="date").text, '%Y/%m/%d %H:%M') < one_day_ago:
            print("已經超出一天，程序停止")
            go = False
            break

        else:
            print("目前畫面最下方文章的日期時間為：",d.find_all(class_="date")[-1].text)
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, "lxml")

        news ={"日期時間":[],"標題":[],"連結":[]}

        for d in soup.find(class_="part_list_2").find_all('h3'):
            if one_day_ago_time in d.find(class_="date") :
               pass
            else:

                news["日期時間"].append(d.find(class_="date").text)
                news["標題"].append(d.find_all('a')[-1].text)
                news["連結"].append("https://www.ettoday.net" + d.find_all('a')[-1]["href"])

browser.close()  #很重要喔記得要關掉瀏覽器．不然要手動關掉

df_news=pd.DataFrame(news)
df_news
#存成csv檔
df_news.to_csv("./df_news1day.csv",encoding='utf-8-sig')


