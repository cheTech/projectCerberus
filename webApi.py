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


class web_Api(object):

    def __init__(self, params, dbObj, handler):
        print("web_Api: Started init...")

        self.db = dbObj

        self.host = params["host"]
        self.port = params["port"]

        self.app = Flask(__name__)
        self.app.logger.addHandler(handler)

        @self.app.errorhandler(Exception)
        def unhandled_exception(e):
            self.app.logger.error('Unhandled Exception: %s', (e))
            return json.dumps({"status": "error", "error": {"reason": "Backend App Error"}}), 500

        @self.app.route("/api/changeUser", methods=["POST"])  # change to POST
        def api_changeUser():
            requestData = json.loads(request.data)

            try:
                self.db.changeUser(userid=requestData["userid"], name=requestData["name"] + " " + requestData["surname"], groupid=requestData["groupid"], pref=requestData["pref"])
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            return json.dumps({"status": "ok"})

        @self.app.route("/api/changeUser", methods=["POST"])  # change to POST
        def api_changeGroup():
            requestData = json.loads(request.data)

            try:
                self.db.changeGroup(groupid=requestData["groupid"], time=requestData["time"], ownerid=requestData["ownerid"], dayofweek=requestData["dayofweek"], cab=requestData["cab"])
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            return json.dumps({"status": "ok"})

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

        @self.app.route("/api/addUser", methods=["POST"])  # change to POST
        def api_addUser():
            requestData = json.loads(request.data)

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

            try:
                self.db.addUser(name=name, groupid=groupid, photopath=imagePath)
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            return json.dumps({"status": "ok"})

        @self.app.route("/api/addGroup", methods=["POST"])  # change to POST
        def api_addGroup():
            requestData = json.loads(request.data)

            try:
                self.db.addGroup(kvant=requestData["kvant"], time=requestData["time"], ownerid=requestData["ownerid"], dayofweek=requestData["dayofweek"], cab=requestData["cab"])
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            return json.dumps({"status": "ok"})

        @self.app.route("/api/deleteUser", methods=["POST"])  # change to POST
        def api_deleteUser():
            requestData = json.loads(request.data)

            try:
                self.db.deleteUser(requestData["userid"])
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

            return json.dumps({"status": "ok"})

        @self.app.route("/api/deleteGroup", methods=["POST"])  # change to POST
        def api_deleteGroup():
            requestData = json.loads(request.data)

            try:
                self.db.deleteGroup(requestData["groupid"])
            except:
                return json.dumps({"status": "error", "error": {"reason": "DatabaseError"}})

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

        Process(target=self.app.run, args=(self.host, self.port)).start()

        print("web_Api: OK!")

    def stop(self):
        print("web_Api: Stopping...")

        self.appProcess.terminate()
        self.appProcess.join()

        print("web_Api: OK!")


if __name__ == "__main__":
    print("Run main.py!")
