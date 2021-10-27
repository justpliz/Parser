import requests
from bs4 import BeautifulSoup
from dateparser import parse
import urllib.request
import time
from datetime import datetime

from Db_connect import original_str_url
from Db_connect import res_id
from Db_connect import insert_item
from Db_connect import cursor_create

url = original_str_url
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
'Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}

def get_html(url, params = None):
    return requests.get(url, headers=HEADERS, params=params)

def html_atributes():
    html_title_tag = ('h3', 'div'),
    html_title_class = ('preview-title preview-title--medium', 'title'),
    html_link_tag = ('a'),
    html_link_class = ('article-preview-mixed', 'title'),
    html_nd_date_tag = ('time'),
    html_nd_date_class = ('preview-info-item-secondary'),
    html_content_tag = ('p'),
    html_content_class = ('align-left formatted-body__paragraph', 'text-align: justify;'),
    html_image_tag = ('img', 'div'),
    html_image_class = ('inline-picture', 'figure-content'),
    html_tags = (html_title_tag, html_title_class, html_link_tag, html_link_class, html_nd_date_tag,
                 html_nd_date_class, html_content_tag, html_content_class, html_image_tag,html_image_class)
    return html_tags


def get_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li' or 'div', class_='block-infinite__item' or 'col-12 col-lg-8')
    return items


def get_titles(items):
    html_tags = html_atributes()
    news = []
    for item in items: #в try  обернуть
        news.append({
            'title': item.find(html_tags[0], class_=html_tags[1]).get_text(strip=True),
            'link': item.find(html_tags[2], class_=html_tags[3]).get('href'),
            'nd_date': item.find(html_tags[4], class_=html_tags[5]).get_text(strip=True),
        })
    return news


def get_content(news, count_url):
    response = urllib.request.urlopen(news[count_url]['link'])
    links_url = response.read()
    soup = BeautifulSoup(links_url, 'html.parser')
    items = soup.find_all('article', class_='article' or 'col-12 col-lg-8')
    html_tags = html_atributes()
    for item in items:
        output_content = []
        output_content.append({
            'content': item.find_all(html_tags[6], class_=html_tags[7]),
            'image': item.find_all(html_tags[8], class_=html_tags[9]),
        })
        return output_content


def parse_news():
    html = get_html(url)
    if html.status_code == 200:
        items = get_items(html.text)
        news = get_titles(items)

        count_url = 0
        cursor_and_connection = cursor_create()
        cursor = cursor_and_connection[0]
        content_news = []
        for i in range(len(items)):
            output_content = get_content(news, count_url)
            content_news.append(output_content)

            content = ''.join(map(str, content_news[count_url]))
            link = ''.join(map(str, news[count_url]['link']))
            title = ''.join(map(str, news[count_url]['title']))
            nd_date = ''.join(map(str, news[count_url]['nd_date']))
            nd_date = parse(nd_date)
            not_date = nd_date.strftime("%Y-%m-%d")
            nd_date = time.mktime(nd_date.timetuple())
            s_date = time.mktime(datetime.now().timetuple())
            insert_item(cursor, res_id, link, title, content, nd_date, s_date, not_date)

            count_url += 1

        connection = cursor_and_connection[1]
        connection.commit()
        cursor.close()
        connection.close()
    else:
        print('Error') #+ статус код

parse_news()

