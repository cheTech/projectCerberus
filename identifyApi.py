"""
Identification Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation:
"""

from time import sleep
from multiprocessing import Process
from threading import Thread
import face_recognition
import cv2
import logging
import json


class identify_Api(object):

    def __init__(self, dbObj, ttsObj, identifyOptions={"cameraid": 0}):
        print("identify_Api: Started init...")

        open("CerberusProjectStatus.txt", "w").write("1")

        self.texttospeech = ttsObj

        self.identifyOptions = identifyOptions

        self.texttospeech = ttsObj

        self.camera = cv2.VideoCapture(self.identifyOptions["cameraid"])

        self.camera.set(3, identifyOptions["res"][0])
        self.camera.set(4, identifyOptions["res"][1])

        self.identifyLoopProcess = Thread(target=self.identify)

        self.identifyActive = True

        self.frameCounter = 0
        self.lastDetected = []

        self.db = dbObj

        self.names, self.encodings = self.db.getNames(), self.db.getEncodings()

        print("identify_Api: OK!")

    def __processMatch(self, match):
        name_data = match

        if name_data["id"] > 0:

            greeting = name_data["pref"]

            if greeting == '':
                greeting = "Привет"

            name = name_data["name"].split(" ")

            self.texttospeech.say("%s %s" % (greeting, name[0]))

            return True

        else:
            print("Unknown Detected")

    def __processCompareFaces(self, face_compare, names):
        for i in range(len(face_compare)):
            if face_compare[i]:
                return names[i]
        return names[0]

    def identify(self):
        self.texttospeech.say("Проект Цербер успешно запущен!")
        while True:
            if self.frameCounter > 30:
                self.lastDetected = []
                self.frameCounter = 0
            else:
                self.frameCounter += 1

            ret, frame = self.camera.read()  # Чтение кадра и состояния камеры
            if ret:  # Если состояние камеры True (все исправно работает)

                # определить положение лиц в кадре
                face_locations = face_recognition.face_locations(frame)

                if face_locations:
                    # определить encoding лиц
                    face_encodings = face_recognition.face_encodings(frame, face_locations)

                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        name = "Unknown"

                        face_compare = face_recognition.compare_faces(self.encodings, face_encoding, tolerance=0.50)

                        points = [(left, top), (right, bottom)]  # x, y текущего лица

                        match = self.__processCompareFaces(face_compare, self.names)

                        # выделить лицо прямоугольником
                        if match["id"] != 0:
                            cv2.rectangle(frame, points[0], points[1], (0, 255, 0), 2)
                        else:
                            cv2.rectangle(frame, points[0], points[1], (0, 0, 255), 2)

                        if self.lastDetected.count(match["id"]) < 1:
                            self.__processMatch(match)

                            self.lastDetected.append(match["id"])

                cv2.imshow("Camera", frame)  # вывод кадра в окно

                key = cv2.waitKey(1) & 0xFF  # Обработка нажатия
                if key == ord("q"):  # кнопки q
                    self.identifyActive = False
                    open("CerberusProjectStatus.txt", "w").write("0")
                    print("quit request")
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
