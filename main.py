"""
Main script.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation:
https://face-recognition.readthedocs.io/en/latest/face_recognition.html
https://docs.opencv.org/4.1.2/
"""

from CerberusApp import CerberusApplication
import logging
import json

# инициализация записи лога
logging.basicConfig(filename='main.log', level=logging.DEBUG)

try:  # Проверка наличия файла с настройками
    settings = json.load(open("settings.json", "r"))  # попытка его загрузки
except Exception as e:
    print(e)
    open("settings.json", "w").write("""{
    "Database Credentials":{
        "dbname":"",
        "dbuser":"",
        "dbpass":"",
        "dbhost":"",
        "table_name_people":"",
        "table_name_groups":""
    },
        "texttospeech Keys":{
        "Yandex SpeechKit Api":"",
        "Google TTS Api":"",
        "Path to local":"",
        "Path to mp3 cache":"temp.mp3"
    },
        "Web Api Settings":{
        "host":"0.0.0.0",
        "port":8080
    },
    "Identify Settings":{
        "cameraid":0,
        "res":[640,360]
    }
}""")  # в противном случае запись файла без данных
    # оповещение пользователя
    print("Open the settings.json and fill in the settings!")
    logging.error("settings.json are empty")  # запись в лог
    exit()  # выход из программы


if __name__ == "__main__":
    CerberusProject = CerberusApplication(settings)
    try:
        CerberusProject.run()
    except KeyboardInterrupt:  # Ctrl-C catch
        CerberusProject.stop()
