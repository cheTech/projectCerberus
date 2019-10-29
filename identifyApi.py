"""
Identification Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation: 
"""

from cv2 import VideoCapture, imshow, waitKey, rectangle
from time import sleep
from multiprocessing import Process
import face_recognition
import logging
import json


class identify_Api(object):

    def __init__(self, people_data, ttsObj, identifyOptions={"cameraid": 0}):
        print("identify_Api: Started init...")

        self.texttospeech = ttsObj

        self.identifyOptions = identifyOptions

        self.texttospeech = ttsObj

        # self.camera = VideoCapture(
        #    self.identifyOptions["cameraid"])  # инициализация камеры

        self.camera = VideoCapture(self.identifyOptions["cameraid"])

        self.camera.set(3, identifyOptions["res"][0])
        self.camera.set(4, identifyOptions["res"][1])

        self.identifyLoopProcess = Process(target=self.identify)

        self.identifyActive = True

        self.names, self.encodings = people_data

        print("identify_Api: OK!")

    def identify(self):
        self.texttospeech.say("Проект Цербер успешно запущен!")
        while True:
            ret, frame = self.camera.read()  # Чтение кадра и состояния камеры
            if ret:  # Если состояние камеры True (все исправно работает)

                # определить положение лиц в кадре
                face_locations = face_recognition.face_locations(frame)

                if len(face_locations) > 0:
                    # определить encoding лиц
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    #
                    for face_encoding in face_encodings:
                        #
                        name = "Unknown"
                        #
                        compared_face = face_recognition.compare_faces(self.encodings, face_encoding, tolerance=0.60)
                        #
                        print(str(compared_face))

                    # обработка положений лиц
                    for (t, r, b, l) in face_locations:
                        points = [(l, t), (r, b)]  # x, y текущего лица
                        # выделить лицо прямоугольником
                        rectangle(frame, points[0], points[1], (0, 255, 0), 2)

                imshow("Camera", frame)  # вывод кадра в окно

                key = waitKey(1) & 0xFF  # Обработка нажатия
                if key == ord("q"):  # кнопки q
                    self.identifyActive = False
                    # break  # выход из цикла -> программы

            else:  # Если камера не работает
                self.texttospeech.say("Ошибка камеры!")
                logging.error("Camera Error")  # запись ошибки камеры в лог
                sleep(5)  # задержка перед повторением цикла

    def run(self):

        print("identify_Api: Running...")

        self.identifyLoopProcess.start()

        print("identify_Api: OK!")

    def stop(self):
        print("identify_Api: Stopping...")

        self.identifyLoopProcess.terminate()
        self.identifyLoopProcess.join()

        print("identify_Api: OK!")


if __name__ == "__main__":
    print("Run main.py!")
