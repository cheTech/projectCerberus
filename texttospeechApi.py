"""
TTS Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation: 
"""

import requests
from playsound import playsound
from threading import Thread
from time import sleep
import json


class texttospeech_Api(object):

    def __init__(self, keys):
        print("texttospeech_Api: Started init...")

        self.yandexkey = keys["Yandex SpeechKit Api"]
        self.googlekey = keys["Google TTS Api"]
        self.pathtolocal = keys["Path to local"]
        self.pathtotmp = keys["Path to mp3 cache"]

        print("texttospeech_Api: OK!")

    def __getVoiceFromYandex(self, text, fileName, format="mp3", lang="ru-RU", speaker="zahar", speed=1, emotion="good"):
        URL = 'https://tts.voicetech.yandex.net/generate?text=%s&format=%s&lang=%s&speaker=%s&key=%s&speed=%s&emotion=%s' % (
            text, format, lang, speaker, self.yandexkey, speed, emotion)  # генерируем ссылку
        response = requests.get(URL)  # посылаем запрос

        if response.status_code == 200:  # если запрос удачен
            # записываем в файл содержимое ответаu
            open(fileName, 'wb').write(response.content)

        return True

    def __say(self, text, engine):  # сказать
        print("texttospeech_Api: Said %s with %s" % (text, engine))  # лог
        if engine == "yandex":  # через Yandex SpeechKit Api
            if self.__getVoiceFromYandex(text=text, fileName=self.pathtotmp):
                playsound(self.pathtotmp)
                return True
            return False
        if engine == "google":  # через gTTS
            return False
        if engine == "local":  # через локальный синтез речи
            return False
        return False  # срабатывает, если что-то идет не так

    def say(self, text, engine="yandex"):  # добавить фразу в очередь на синтез
        Thread(target=self.__say, args=(text, engine)).run()

    def run(self):  # запуск цикла
        print("texttospeech_Api: Running...")

        # self.voiceLoopProcess.start()

        print("texttospeech_Api: OK!")

    def stop(self):
        print("texttospeech_Api: Stopping...")

        # self.voiceLoopProcess.terminate()
        # self.voiceLoopProcess.join()

        print("texttospeech_Api: OK!")


if __name__ == "__main__":
    print("Run main.py!")
