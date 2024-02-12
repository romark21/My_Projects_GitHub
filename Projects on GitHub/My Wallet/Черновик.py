from time import sleep
from random import uniform
import requests
import pandas as pd
from bs4 import BeautifulSoup
import fake_useragent
import re


def get_authoriz_and_authentic():
    username = input('Введите username: ')
    password = input('Введите password: ')
    url = 'https://my.e-klase.lv/?v=15'
    user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': user_agent}
    user_data = {
        'UserName': str(username),
        'Password': str(password)
    }

    with requests.session() as session:
        session.get(url)
        response = session.post(url, data=user_data, headers=header)
        if response.status_code == 200:
            cookies = response.cookies.get_dict()
            print('Authorization passed - Successful!\n'
                  'Авторизация прошла - Успешно!')
            print('*' * 60)
        else:
            print('Error when sending a request for authorization!\n'
                  'Ошибка при отправке запроса для авторизации!')
            print('*' * 60)

        sleep(uniform(3, 6))

        # Go to the page with the buttons(Select a user profile), using cookies
        buttons_url = 'https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd'
        response = session.get(buttons_url, cookies=cookies)
        if response.status_code == 200:
            print('Selecting a user profile - Successful!\n'
                  'Выбор пользовательского профиля - Успешно!')
            print('*' * 60)
        else:
            print('Error when sending a request in the user profile selection window!\n'
                  'Ошибка при отправке запроса в окне выбора профиля пользователя!')
            print('*' * 60)

        sleep(uniform(3, 6))

        # Go to the Diary page, using cookies.
        diary = 'https://my.e-klase.lv/Family/Diary'
        diary = re.sub(r'>\s+<', '><', diary.replace('\n', ''))
        response = session.get(diary, cookies=cookies)
        if response.status_code == 200:
            print('Going to the "Diary" page - Successful!\n'
                  'Переход на страницу "Дневник" - Успешно!\n')
            print('*' * 60)
        else:
            print('Error when sending request, tab - "Diary"!\n'
                  'Ошибка при отправке запроса, вкладка - "Дневник"!')
            print('-' * 60)

        # Prompt the user for information about the week selection.
        user_week_data = input(f'Укажите за какую неделю вы хотите получить данные!\n1 - За текущую неделю\n'
                               f'2 - За следующию неделю\n'
                               f'Введите число: ')
        soup = BeautifulSoup(response.text, 'lxml')

        if user_week_data == '1':
            soup = soup
        elif user_week_data == '2':
            sleep(uniform(3, 6))
            next_week_url = soup.find('div', class_='week-selector clearfix').find_all('a')[-1].get('href')
            response = session.get('https://my.e-klase.lv/' + next_week_url,
                                   cookies=cookies)  # Check out next week's page
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
            else:
                print("Error submitting a request about next week's information!\n"
                      "Ошибка при отправке запроса для получения данных о следующей недели!")
                print('*' * 60)
        else:
            print('Вы ввели неправильную команду!')

        return soup


def get_diary_datas_per_day():
    week_data = get_authoriz_and_authentic().find('div', class_='student-journal-lessons-table-holder hidden-xs')
    dates = week_data.find_all('h2')  # Get all dates per week
    dates_list = [date.text.strip() for date in dates]  # List with formatted dates
    count = 0
    day_data = week_data.find_all('table', class_='lessons-table')
    for i in day_data:
        print()
        print()
        print()
        print(f'<<<<<<<<<<   {dates_list[count]}   >>>>>>>>>>')
        print()
        lessons_data = i.find('tbody').find_all('tr')
        count += 1

        for j, datas in enumerate(lessons_data, 1):
            try:
                lesson_name = datas.find('span', class_='room')
                lesson_name = lesson_name.previous_element.text.strip()
            except AttributeError:
                lesson_name = ''

            try:
                lesson_topic = datas.find('td', class_='subject').text.strip()
            except AttributeError:
                lesson_topic = ''

            try:
                home_task_1 = datas.find('span', class_='ThirdPartyEvent__EventName').get_text(strip=True)
            except AttributeError:
                home_task_1 = ''
            if home_task_1 == '':
                try:
                    home_task_2 = datas.find('td', class_='hometask').text.strip()
                # hometask_2 = hometask_2.next_element.text.strip()
                except AttributeError:
                    home_task_2 = ''
            else:
                home_task_2 = ''

            try:
                score = datas.find('span', class_='score').text.strip()
            except AttributeError:
                score = ''

            result = (f'{j})\n<<< {lesson_name} >>>\n- Тема урока: "{lesson_topic}"\n'
                      f'- Домашнее задание: "{home_task_1}{home_task_2}"\n'
                      f'- Оценка: {score}')

            yield result


class Week:
    def __init__(self, name):
        self.name = name

    def get_panel_data(self, data):
        df = pd.DataFrame(data)
        return df

    def save_data_csv(self, data):
        save_data = data.to_csv(f'{self.name}.csv', mode='w', index=False, header=True)
        return save_data

    def overwrite_data_csv(self, data):
        overwrite_data = data.to_csv(f'{self.name}.csv', mode='a', index=False, header=False)
        return overwrite_data


def get_result(func):
    datas_for_save = []
    for data in func:
        print(f'{data}')
        print('---' * 20)
        datas_for_save.append(data)
    return datas_for_save


if __name__ == '__main__':
    this_week = Week('This_week')
    next_week = Week('Next_week')
    print(get_result(get_diary_datas_per_day()))
