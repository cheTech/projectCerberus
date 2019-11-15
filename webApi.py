"""
Web Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation:
"""

from flask import Flask, request, render_template
from utils import fromBase64imgToFile, normalizeEncoding
import json
import os
import face_recognition
import cv2
from multiprocessing import Process
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'flask.log'
    LOGGING_LEVEL = logging.DEBUG


class web_Api(object):

    def __init__(self, params, dbObj):
        print("web_Api: Started init...")

        self.db = dbObj

        self.host = params["host"]
        self.port = params["port"]

        self.app = Flask(__name__)
        handler = logging.FileHandler("flask.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.app.logger.addHandler(handler)

        @self.app.errorhandler(Exception)
        def unhandled_exception(e):
            self.app.logger.error('Unhandled Exception: %s', (e))
            return json.dumps({"status": "error", "error": {"reason": "Backend App Error"}}), 500

        @self.app.route("/api/getUsers", methods=["GET"])  # change to POST
        def api_getUsers():
            try:
                usersFullData = self.db.getNames()
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            try:
                startIndex = int(request.args.get("start"))
            except:
                startIndex = 0

            try:
                endIndex = int(request.args.get("end"))
            except:
                endIndex = len(usersFullData)

            if endIndex > len(usersFullData):
                endIndex = len(usersFullData)

            usersData = usersFullData[startIndex:endIndex]

            return json.dumps({"status": "ok", "items": usersData})

        @self.app.route("/api/getGroups", methods=["GET"])  # change to POST
        def api_getGroups():
            try:
                groupsData = self.db.getGroups()
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            return json.dumps({"status": "ok", "items": groupsData})

        @self.app.route("/api/getGroupInfo", methods=["GET"])  # change to POST
        def api_getGroupInfo():
            try:
                groupId = int(request.args.get("groupId"))
            except:
                return json.dumps({"status": "error", "error": {"reason": "Bad groupId parameter!"}})

            try:
                data = self.db.getGroupInfo(groupId)
            except:
                return json.dumps({"status": "error", "error": {"reason": "Ошибка базы данных!"}})

            return json.dumps({"status": "ok", "items": data})

        @self.app.route("/api/addUser", methods=["POST"])  # change to POST
        def api_addUser():
            requestData = request.get_json()

            imagePath = "temp.jpg"
            fromBase64imgToFile(requestData["photo"], imagePath)
            image = cv2.imread(imagePath)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) > 1:
                return json.dumps({"status": "error", "error": {"reason": "Лиц на фото - %s, должно быть 1!" % (len(face_locations))}})
            if len(face_locations) < 1:
                return json.dumps({"status": "error", "error": {"reason": "На фото не обнаружено лица!"}})

            name = requestData["name"] + " " + requestData["surname"]
            groupid = requestData["groupid"]

            self.db.addUser(name=name, groupid=groupid, photopath=imagePath)

            return json.dumps({"status": "ok"})

        @self.app.route("/api/addGroup", methods=["POST"])  # change to POST
        def api_addGroup():
            #requestData = request.get_json()
            requestData = json.loads(request.data)

            self.db.addGroup(kvant=requestData["kvant"], time=requestData["time"], ownerid=requestData["ownerid"], dayofweek=requestData["dayofweek"], cab=requestData["cab"])

            return json.dumps({"status": "ok"})

        @self.app.route("/api/deleteUser", methods=["POST"])  # change to POST
        def api_deleteUser():
            #requestData = request.get_json()
            requestData = json.loads(request.data)

            self.db.deleteUser(requestData["userid"])

            return json.dumps({"status": "ok"})

        @self.app.route("/api/deleteGroup", methods=["POST"])  # change to POST
        def api_deleteGroup():
            requestData = request.get_json()

            self.db.deleteGroup(requestData["groupid"])

            return json.dumps({"status": "ok"})

        @self.app.route("/add/user")
        def add_user():
            return render_template("addNewUser.html")

        @self.app.route("/add/group")
        def add_group():
            return render_template("addNewGroup.html")

        @self.app.route("/view/users")
        def view_users():
            return render_template("viewUsers.html")

        @self.app.route("/view/groups")
        def view_groups():
            return render_template("viewGroups.html")

        @self.app.route("/dashboard")
        def dashboard():
            return render_template("dashboard.html")

        print("web_Api: OK!")

    def run(self):
        print("web_Api: Running...")

        #Process(target=self.app.run, args=(self.host, self.port)).start()
        self.app.run(host="0.0.0.0")

        print("web_Api: OK!")

    def stop(self):
        print("web_Api: Stopping...")

        self.appProcess.terminate()
        self.appProcess.join()

        print("web_Api: OK!")


if __name__ == "__main__":
    print("Run main.py!")
