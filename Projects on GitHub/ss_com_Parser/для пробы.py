import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import fake_useragent


user_agen = fake_useragent.UserAgent().random
head = {"User-Agent": user_agen}


with requests.session() as session:
    res = session.get('https://www.ss.com/ru/transport/cars/bmw/', headers=head)
    soups = BeautifulSoup(res.text, 'lxml')
    datas = soups.find_all('div', class_='d1')
    print('1' * 30)
    print(datas)
    print('1' * 30)

    for data in datas:
        card_url = data.find('a')
        print('2' * 30)
        print(card_url)
        print('2' * 30)
        if card_url is not None:
            url = 'https://www.ss.lv' + card_url.get('href')
            print('3' * 30)
            print(url)
            print('3' * 30)


