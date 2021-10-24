import requests
from bs4 import BeautifulSoup
from dateparser import parse
import urllib.request


from Db_connect import originalStrURL
from Db_connect import insert_varibles_into_table

URL = originalStrURL
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
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

# def blabla(self, nd_date):
#     self.nd_date = nd_date
#     parse(nd_date)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        news = get_content(html.text)

        link = ''.join(map(str, news[0]['link']))
        title = ''.join(map(str, news[0]['title']))
        content = ''.join(map(str, news[1]['content']))
        nd_date = ''.join(map(str, news[0]['nd_date']))
        # nd_date = nd_date
        # parse(nd_date)
        # blabla(nd_date)
        #date_int(nd_date)
        insert_varibles_into_table(1, 1, link, title, content, nd_date, nd_date, nd_date)
    else:
        print('Error')

parse()

