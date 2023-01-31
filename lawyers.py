import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

class NotValidPageNumber(Exception):
    pass

URL = 'http://lawyers.minjust.ru/Lawyers'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'
}

def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req

def get_content(html):
    soup = BS(html, 'html.parser')
    table = soup.find('table', class_='persons')
    pages = []
    for line in table.find_all('tr')[1:]:
        row_data = line.find_all('td')
        row = [el.text for el in row_data]
        pages.append(row)
    return pages

def parsing(url):
    while True:
        try:
            print('Enter the start page number for parsing:', end=' ')
            start = int(input())
            print('Enter the end page number for parsing:', end=' ')
            end = int(input())
            if end < start:
                raise NotValidPageNumber
            break
        except ValueError:
            print('ERROR: Page number must be an integer\nTry again')
        except NotValidPageNumber:
            print('ERROR: The last page number cannot be greater than the start page number\nTry again')

    lawyers = []
    for page in range(start - 1, end):
        print(f'Parsing page: {page + 1}')
        html = get_html(url, params={'page': page})
        lawyers.extend(get_content(html.text))
    return lawyers

def save_doc(url):
    html = get_html(url)
    soup = BS(html.text, 'html.parser')
    table = soup.find('table', class_='persons')
    thead = []

    for column in table.find_all('th'):
        thead.append(column.text)
    lawyers = pd.DataFrame(columns=thead)

    for row in parsing(url):
        lenght = len(lawyers)
        lawyers.loc[lenght] = row
    lawyers.to_excel('lawyers.xlsx', index=False)

save_doc(URL)
