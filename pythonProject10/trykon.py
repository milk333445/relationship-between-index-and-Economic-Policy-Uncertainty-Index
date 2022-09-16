import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import  pandas as pd
import jieba

#options=webdriver.ChromeOptions()
#options.add_argument('--headless')
#driver=webdriver.Chrome('./chromedriver', options=options)
page1=input('data-page=')
page1=int(page1)
post_dict = {'date':[], 'title':[], 'url':[], 'news':[]}
keyword='經濟'
for page in range(1, page1+1):
    url = ('https://www.chinatimes.com/newspapers/2602?page=' + str(page))
    url2=('https://www.chinatimes.com/search/{}?page={}'.format(keyword,page))
    print(url2)
    response = requests.get(url2)
    soup = BeautifulSoup(response.text, 'lxml')
    for ele in soup.find('ul', 'vertical-list list-style-none').find_all('li'):
        title = ele.find('h3').text.strip()
        date=ele.find('span','date').text.strip()
        url=ele.a['href']
        post_dict['date'].append(date)
        post_dict['title'].append(title)
        post_dict['url'].append(url)
        try:
            '''driver.get(http)
            source1=driver.page_source
            soup1=BeautifulSoup(source1,'html.parser')'''
            # posts1=soup1.find('div','cont').find_all('p')
            # posts1 = soup1.find_all('p')
            posts1 = ele.find_all('p')
            content = ''
            for p in posts1:
                content += p.text
            post_dict['news'].append(content)
        except:
            post_dict['news'].append('')
post_df = pd.DataFrame(post_dict)
post_df.to_csv('工商時報經濟.csv',encoding='utf-8-sig',index=False)