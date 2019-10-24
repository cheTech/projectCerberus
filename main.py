"""
Main script of face identification.

Author: cheTech
GitHub: https://github.com/cheTech/itkvant-robot

Documentation:
https://face-recognition.readthedocs.io/en/latest/face_recognition.html
https://docs.opencv.org/4.1.2/
"""

from cv2 import VideoCapture, imshow, waitKey, rectangle, destroyAllWindows
from time import sleep
from databaseApi import DatabaseApi
from texttospeechApi import TTSApi
import face_recognition
import logging
import json

try:  # Проверка наличия файла с настройками
    settings = json.load(open("settings.json", "r"))  # попытка его загрузки
except:
    open("settings.json", "w").write("""{
    "Database Credentials":{
        "dbname":"",
        "dbuser":"",
        "dbpass":"",
        "dbhost":"",
        "table_name":""
    },
    "texttospeech Keys":{
    "Yandex SpeechKit Api":"",
    "Google TTS Api":"",
    "Path to local":"",
    "Path to mp3 cache":"temp.mp3"
    }
}""")  # в противном случае запись файла без данных
    # оповещение пользователя
    print("Open the settings.json and fill in the settings!")
    logging.error("settings.json are empty")  # запись в лог
    exit()  # выход из программы

db = DatabaseApi(settings["Database Credentials"])  # инициализация базы данных
tts = TTSApi(settings["texttospeech Keys"])  # инициализация синтеза речи

# инициализация записи лога
logging.basicConfig(filename='main.log', level=logging.DEBUG)

camera = VideoCapture(0)  # инициализация камеры


class CerberusApp(object):

    def __init__(self):
        print('Successful init')
        TTSApi.say("projectCerber инициализирован")

    def identify(self):
        while True:
            ret, frame = camera.read()  # Чтение кадра и состояния камеры
            if ret:  # Если состояние камеры True (все исправно работает)
                # определить положение лиц в кадре
                face_locations = face_recognition.face_locations(frame)
                # определить encoding лица
                face_encodings = face_recognition.face_encodings(
                    frame, face_locations)

                # обработка положений лиц
                for (t, r, b, l) in face_locations:
                    points = [(l, t), (r, b)]  # x, y текущего лица
                    # выделить лицо прямоугольником
                    rectangle(frame, points[0], points[1], (0, 255, 0), 2)

                imshow("Camera", frame)  # вывод кадра в окно

                key = waitKey(1) & 0xFF  # Обработка нажатия
                if key == ord("q"):  # кнопки q
                    break  # выход из цикла -> программы

            else:  # Если камера не работает
                logging.error("Camera Error")  # запись ошибки камеры в лог
                sleep(1)  # задержка перед повторением цикла

        camera.release()  # закрытие видеопотока с камеры
        destroyAllWindows()  # закрыть все окна

    def webApi(self):
        print("*flask started*")

    def run(self):
        self.identify()
        self.webApi()

if __name__ == "__main__":
    CerberusApp().run()
