import requests
import dateparser
from bs4 import BeautifulSoup

URL = 'https://www.nur.kz/society/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
'Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='block-infinite__item')


    news = []
    for item in items:
        news.append({
            'title': item.find('h3', class_='preview-title preview-title--medium').get_text(strip=True),
            'link': item.find('a', class_='article-preview-mixed').get('href'),
            'data': item.find('time', class_='preview-info-item-secondary').get_text(strip=True),
            #'content':
        })

        print(news)
        return news



    IncludeContent = []
    for i in range(0, len(news)):
        IncludeContent.append({
            'content': item.find
        })

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        news = get_content(html.text)
    else:
        print('Error')

parse()