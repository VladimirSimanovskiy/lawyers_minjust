import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

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

    for line in table.find_all('tr')[1:]:
        row_data = line.find_all('td')
        row = [el.text for el in row_data]
        lenght = len(lawyers)
        lawyers.loc[lenght] = row
    return lawyers


def parsing(frame):
    soup = BS(get_html(URL), 'html.parser')
    table = soup.find('table', class_='persons')
    thead = []

    for column in table.find_all('th'):
        thead.append(column.text)

    lawyers = pd.DataFrame(columns=thead)

    for page in range(0, 5):
        print(f'Парсим страницу: {page}')
        html = get


    # frame.to_excel('lawyers.xlsx', index=False)


frame = get_content(html.text)
parsing(frame)