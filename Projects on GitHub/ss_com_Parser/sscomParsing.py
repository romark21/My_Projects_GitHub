import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import fake_useragent

user_agent = fake_useragent.UserAgent().random
headers = {"User-Agent": user_agent}
# def main():
#     url = f'https://www.ss.com/ru/transport/cars/bmw.html'
#     get_url(url)
print(f'{"-" * 10}\nAlfa Romeo, Audi\n{"-" * 40}\n'
      f'BMW\n{"-" * 40}\n'
      f'Chevrolet, Chrysler, Citroen\n{"-" * 40}\n'
      f'Dacia, Dodge\n{"-" * 40}\n'
      f'Fiat, Ford\n{"-" * 40}\n'
      f'Honda, Hyundai\n{"-" * 40}\n'
      f'Infiniti\n{"-" * 40}\n'
      f'Jaguar, Jeep\n{"-" * 40}\n'
      f'Kia\n{"-" * 40}\n'
      f'Lancia, Land Rover, Lexus\n{"-" * 40}\n'
      f'Mazda, Mercedes, Mini, Mitsubishi\n{"-" * 40}\n'
      f'Nissan\n{"-" * 40}\n'
      f'Opel\n{"-" * 40}\n'
      f'Peugeot, Porsche\n{"-" * 40}\n'
      f'Renault\n{"-" * 40}\n'
      f'Saab, Seat, Skoda, Smart, Subaru, Suzuki\n{"-" * 40}\n'
      f'Toyota\n{"-" * 40}\n'
      f'Volkswagen, Volvo\n{"-" * 40}\n'
      f'Vaz, Gaz, Uaz\n{"-" * 40}\n'
      f'Others\n{"-" * 10}\n')
brand_auto = input(f"Enter vehicle name to get a list of ads: ").lower()
print()


def get_url():
    count = 1
    while count < 2:
        url = f'https://www.ss.com/ru/transport/cars/{brand_auto}/page{count}.html'
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        datas = soup.find_all('div', class_='d1')
        count += 1
        for data in datas:
            card_url = data.find('a')
            if not card_url:
                continue
            url = 'https://www.ss.lv' + card_url.get('href')
            yield url


for i, url in enumerate(get_url(), 1):
    response = requests.get(url, headers=headers)
    sleep(2)
    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find('div', {'id': 'msg_div_msg'})

    try:
        year = data.find('td', {'id': 'tdo_18'}).text
    except AttributeError:
        year = "--------"

    try:
        model = data.find('td', {'id': 'tdo_31'}).text
    except AttributeError:
        model = "--------"

    try:
        motor = data.find('td', {'id': 'tdo_15'}).text
    except AttributeError:
        motor = "--------"

    try:
        transmission = data.find('td', {'id': 'tdo_35'}).text
    except AttributeError:
        transmission = "--------"

    try:
        car_mileage = data.find('td', {'id': 'tdo_16'}).text
    except AttributeError:
        car_mileage = "--------"

    try:
        color = data.find('td', {'id': 'tdo_17'}).text
    except AttributeError:
        color = "--------"

    try:
        car_body = data.find('td', {'id': 'tdo_32'}).text
    except AttributeError:
        car_body = "--------"

    try:
        technical_inspection = data.find('td', {'id': 'tdo_223'}).text
    except AttributeError:
        technical_inspection = "--------"

    del_str = data.text.find('Марка')
    description = re.sub(r"^\s+|\n|\r|", '', data.text[:del_str])

    print(f'{i})\nModel: {model}\n{"-" * 20}\nYear: {year}\n{"-" * 20}\nMotor: {motor}\n{"-" * 20}\n'
          f'Transmission: {transmission}\n{"-" * 20}\nCar body: {car_body}\n{"-" * 20}\nColor: {color}\n{"-" * 20}\n'
          f'Run rate: {car_mileage} км.\n{"-" * 20}\nTech.Inspection: {technical_inspection}\n{"-" * 20}\n'
          f'Description: {description}\n{url}\n{"-" * 60}\n')
    print()

