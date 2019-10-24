import requests
from playsound import playsound
from threading import Thread


class TTSApi(object):

    def __init__(self, keys):
        self.yandexkey = keys["Yandex SpeechKit Api"]
        self.googlekey = keys["Google TTS Api"]
        self.pathtolocal = keys["Path to local"]
        self.pathtolocal = keys["Path to mp3 cache"]

        self.speechQuery = []  # очередь на синтез
        print("Successful TTSApi initialization.")

    def __getVoiceFromYandex(text, fileName, format="mp3", lang="ru-RU", speaker="zahar", speed=1, emotion="good"):
        URL = 'https://tts.voicetech.yandex.net/generate?text=%s&format=%s&lang=%s&speaker=%s&key=%s&speed=%s&emotion=%s' % (
            text, format, lang, speaker, self.yandexkey, speed, emotion)  # генерируем ссылку
        response = requests.get(URL)  # посылаем запрос

        if response.status_code == 200:  # если запрос удачен
            # записываем в файл содержимое ответа
            open(fileName, 'wb').write(response.content)

        return True

    def __say(self, text, engine):  # сказать
        print("Said %s with %s" % (text, engine))  # лог
        if engine == "yandex":  # через Yandex SpeechKit Api
            return False
        if engine == "google":  # через gTTS
            return False
        if engine == "local":  # через локальный синтез речи
            return False
        return False  # срабатывает, если что-то идет не так

    def __voiceLoop(self):  # цикл обрабатывающий очередь на синтез речи
        while True:
            if len(self.speechQuery) > 0:  # если очередь не пустая
                for text, engine in self.speechQuery:
                    self.__say(text=text, filename=self.filename,
                               engine=engine)
                self.speechQuery = []  # обнулить очередь

    def say(self, text, engine="yandex"):  # добавить фразу в очередь на синтез
        self.speechQuery.append([text, engine])

    def run(self):  # запуск цикла
        voiceLoopThread = Thread(target=self.__voiceLoop)
        voiceLoopThread.start()
