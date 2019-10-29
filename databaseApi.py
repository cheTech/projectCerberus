"""
Database Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation:
"""

import psycopg2
from multiprocessing import Process
import numpy as np
import json
import pickle
import base64


class database_Api(object):

    def __init__(self, credentials):
        print("database_Api: Started init...")
        self.credentials = credentials
        self.conn = psycopg2.connect(dbname=self.credentials["dbname"], user=self.credentials[
            "dbuser"], password=self.credentials["dbpass"], host=self.credentials["dbhost"])  # подключаемся к базе данных
        self.cursor = self.conn.cursor()
        print("database_Api: OK!")

    def __decode(self, string):
        decoded_string = base64.b64decode(string)
        return pickle.loads(decoded_string)

    def getNames(self):  # запрос имен
        # выполняем запрос по таблице с данными пользователей с сортировкой по
        # идентификатору
        self.cursor.execute("SELECT id,name,groupid,deleted,photo,pref FROM %s ORDER BY id" % (
            self.credentials["table_name_people"]))
        dbData = self.cursor.fetchall()  # парсим ответ

        dataNames = []

        for data in dbData:
            dataNames.append({"id": data[0],
                              "name": data[1],
                              "groupid": data[2],
                              "deleted": data[3],
                              "photo": data[4],
                              "pref": data[5]})

        return dataNames

    def getEncodings(self):  # запрос encoding`ов лиц
        # выполняем запрос по таблице с данными пользователей с сортировкой по
        # идентификатору
        self.cursor.execute("SELECT face_encoding FROM %s ORDER BY id" % (
            self.credentials["table_name_people"]))
        dbData = self.cursor.fetchall()  # парсим ответ

        dataEncodings = []

        for encoding in dbData:
            dataEncodings.append(np.array(json.loads(encoding[0])))

        dataEncodings = np.array(dataEncodings).reshape((128))

        print(dataEncodings.shape)

        return dataEncodings

    def getGroups(self):

        return []


if __name__ == "__main__":
    print("Run main.py!")
