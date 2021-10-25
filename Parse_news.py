import requests
from bs4 import BeautifulSoup
from dateparser import parse
import urllib.request
import time
from datetime import datetime

from Db_connect import original_str_url
from Db_connect import insert_item

url = original_str_url
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
'Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}

def get_html(url, params = None):
    return requests.get(url, headers=HEADERS, params=params)

def get_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='block-infinite__item')
    return  items

def get_titles(items):
    news = []
    for item in items: #в try  обернуть
        news.append({
            'title': item.find('h3', class_='preview-title preview-title--medium').get_text(strip=True),
            'link': item.find('a', class_='article-preview-mixed').get('href'),
            'nd_date': item.find('time', class_='preview-info-item-secondary').get_text(strip=True),
        })
    return news


def get_content(news, count):
    response = urllib.request.urlopen(news[count]['link'])
    links_url = response.read()
    soup = BeautifulSoup(links_url, 'html.parser')
    items = soup.find_all('article', class_='article')
    output_content = []
    for item in items:
        output_content.append({
            'content': item.find_all('p', class_='align-left formatted-body__paragraph'),
            'image': item.find_all('img', class_='inline-picture'),
        })
        return output_content


def parse_news():
    html = get_html(url)#responce atribute
    if html.status_code == 200: #200 в константу
        items = get_items(html.text)
        count = len(items)
        for i in items:
            count += 1
        news = get_titles(items, count)
        output_content = get_content(news)

        #news += output_content

        link = ''.join(map(str, news[0]['link']))
        title = ''.join(map(str, news[0]['title']))
        content = ''.join(map(str, output_content[0]['content']))
        nd_date = ''.join(map(str, news[0]['nd_date']))
        nd_date = parse(nd_date)
        not_date = nd_date.strftime("%Y-%m-%d")
        nd_date = time.mktime(nd_date.timetuple())
        s_date = time.mktime(datetime.now().timetuple())

        #insert_item(1, link, title, content, nd_date, s_date, not_date)
    else:
        print('Error') #+ статус код

parse_news()

