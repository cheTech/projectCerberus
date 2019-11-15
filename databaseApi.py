"""
Database Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation:
"""
from multiprocessing import Process
from utils import normalizeEncoding
import numpy as np
import psycopg2
import json
import pickle
import base64
import shutil
import face_recognition
import cv2


class database_Api(object):

    def __init__(self, credentials):
        print("database_Api: Started init...")
        self.credentials = credentials
        self.conn = psycopg2.connect(dbname=self.credentials["dbname"], user=self.credentials[
            "dbuser"], password=self.credentials["dbpass"], host=self.credentials["dbhost"])  # подключаемся к базе данных
        self.cursor = self.conn.cursor()
        print("database_Api: OK!")

    def deleteUser(self, userid):
        self.cursor.execute("UPDATE %s SET deleted=1 WHERE id=%s" % (self.credentials["table_name_people"], userid))

        self.conn.commit()

        return True

    def deleteGroup(self, groupid):
        self.cursor.execute("UPDATE %s SET deleted=1 WHERE id=%s" % (self.credentials["table_name_groups"], groupid))

        self.conn.commit()

        return True

    def addUser(self, name, groupid, photopath, pref=""):
        iden = int(self.getNames()[-1]["id"]) + 1
        deleted = 0

        newPhotoPath = "static/img/people/%s.jpg" % (iden)
        shutil.copy(photopath, newPhotoPath)

        image = cv2.imread(newPhotoPath)
        face_locations = face_recognition.face_locations(image)
        face_encoding = normalizeEncoding(face_recognition.face_encodings(image, face_locations)[0])

        self.cursor.execute("INSERT INTO %s (id,name,groupid,deleted,photo,pref,face_encoding) VALUES (%s,'%s',%s,%s,'%s','%s','%s')" % (self.credentials["table_name_people"], iden, name, groupid, deleted, newPhotoPath, pref, face_encoding))

        self.conn.commit()

        return True

    def addGroup(self, kvant, time, ownerid, dayofweek, cab, deleted=0):
        iden = int(self.getGroups()[-1]["id"]) + 1

        self.cursor.execute("INSERT INTO %s (id,kvant, time, ownerid, deleted, dayofweek, cab) VALUES (%s,'%s','%s',%s,%s,%s,%s)" % (self.credentials["table_name_groups"], iden, kvant, time, ownerid, deleted, dayofweek, cab))

        self.conn.commit()

        return True

    def getNames(self, groupid=None, withDeleted=False):  # запрос имен
        # выполняем запрос по таблице с данными пользователей с сортировкой по
        # идентификатору
        if groupid:
            self.cursor.execute("SELECT id,name,groupid,deleted,photo,pref FROM %s WHERE groupid=%s ORDER BY id" % (
                self.credentials["table_name_people"], groupid))
        else:
            self.cursor.execute("SELECT id,name,groupid,deleted,photo,pref FROM %s ORDER BY id" % (
                self.credentials["table_name_people"]))
        dbData = self.cursor.fetchall()  # парсим ответ

        dataNames = []

        for data in dbData:
            if withDeleted:
                dataNames.append({"id": data[0],
                                  "name": data[1],
                                  "groupid": data[2],
                                  "deleted": data[3],
                                  "photo": data[4],
                                  "pref": data[5]})
            else:
                if data[3] == 0:
                    dataNames.append({"id": data[0],
                                      "name": data[1],
                                      "groupid": data[2],
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
            enc = np.array(json.loads(encoding[0]))
            dataEncodings.append(enc)

        return dataEncodings

    def getGroups(self):
        dataGroups = []

        self.cursor.execute("SELECT * FROM %s ORDER BY id" % (
            self.credentials["table_name_groups"]))
        dbData = self.cursor.fetchall()  # парсим ответ

        for data in dbData:
            dataGroups.append({
                "id": data[0],
                "kvant": data[1],
                "time": data[2],
                "ownerid": data[3],
                "deleted": data[4],
                "dayofweek": data[5]
            })

        return dataGroups


if __name__ == "__main__":
    print("Run main.py!")
