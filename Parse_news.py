import requests
from bs4 import BeautifulSoup
from dateparser import parse
import urllib.request
import time
from datetime import datetime

from Db_connect import original_str_url
from Db_connect import insert_item


URL = original_str_url
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
'Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}


def get_html(url, params = None):  # TODO тайпинг и что возвращает функция
    return requests.get(url, headers=HEADERS, params=params)


def get_content(html):  # TODO тайпинг и что возвращает функция
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='block-infinite__item')
    
    news = []
    for item in items: #в try  обернуть
        news.append({
            'title': item.find('h3', class_='preview-title preview-title--medium').get_text(strip=True),
            'link': item.find('a', class_='article-preview-mixed').get('href'),
            'nd_date': item.find('time', class_='preview-info-item-secondary').get_text(strip=True),
        })

        response = urllib.request.urlopen(news[0]['link'])
        linksURL = response.read()
        soup = BeautifulSoup(linksURL, 'html.parser')
        items = soup.find_all('article', class_='article')
        
        outputContent = []
        for item in items:
             outputContent.append({
                'content': item.find_all('p', class_='align-left formatted-body__paragraph'),
                'image': item.find_all('img', class_='inline-picture'),
             })

        news += outputContent
        return news


def parse_news():
    html = get_html(URL)  # responce atribute
    
    if html.status_code == 200:  # 200 в константу
        news = get_content(html.text)

        link = ''.join(map(str, news[0]['link']))
        title = ''.join(map(str, news[0]['title']))
        content = ''.join(map(str, news[1]['content']))
        nd_date = ''.join(map(str, news[0]['nd_date']))
        nd_date = parse(nd_date)
        not_date = nd_date.strftime("%Y-%m-%d")
        nd_date = time.mktime(nd_date.timetuple())
        s_date = time.mktime(datetime.now().timetuple())

        insert_item(1, link, title, content, nd_date, s_date, not_date)
    else:
        print('Error')  # + статус код

parse_news()

