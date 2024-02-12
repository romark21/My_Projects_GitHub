
import json
import queue
import speech_recognition as sr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import comands
import voice

import vosk
import pyaudio
q = queue.Queue()
r = sr.Recognizer()
sr.pause_threshold = 0.5


def listen_comand():
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, 0.5)
        print("Говорите...")
        audio = r.listen(mic)

    try:
        query = r.recognize_google(audio, language='ru-RU').lower()
        print("сейчас напичатаю")
        return query

    except sr.UnknownValueError:
        return ("Чего?   Прожуй, а потом говори. Мотхер фуцкер!")
    except sr.RequestError as e:
        return ('Проблема с сервисом Google: {0}'.format(e))


def recognizer(data, vectorizer, clf):
    trig = comands.TRIGGERS.intersection(data.split())
    if not trig:
        return
    # удаляем имя бота из текста
    data.replace(list(trig)[0], '')

    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    # озвучка ответа из модели data_set
    # voice.speaker(answer.replace(func_name, ''))

    # запуск функции из skills
    exec(func_name + '()')


def callback(indata, frames, time, status):
    '''
    Добавляет в очередь семплы из потока.
    вызывается каждый раз при наполнении blocksize
    в sd.RawInputStream'''

    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    '''
    Анализ распознанной речи
    '''

    # проверяем есть ли имя бота в data, если нет, то return
    trg = comands.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # удаляем имя бота из текста
    data.replace(list(trg)[0], '')

    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    # озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name, ''))

    # запуск функции из skills
    exec(func_name + '()')


def main():
    '''
    Обучаем матрицу ИИ
    и постоянно слушаем микрофон
    '''

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # постоянная прослушка микрофона
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, 0.5)
        print("Говорите...")
        audio = r.listen(mic)

    try:
        query = r.recognize_google(audio, language='ru-RU').lower()
        print("сейчас напичатаю")
        return query

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
            # else:
            #     print(rec.PartialResult())


if __name__ == '__main__':
    main()
