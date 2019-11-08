"""
Web Api.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation:
"""

from multiprocessing import Process
from flask import Flask, request
import json
import os


class web_Api(object):

    def __init__(self, params, dbObj):
        print("web_Api: Started init...")

        self.db = dbObj

        self.host = params["host"]
        self.port = params["port"]

        self.app = Flask(__name__)
        self.appProcess = Process(target=self.__run)

        @self.app.route("/api/getUsers", methods=["GET"])  # change to POST
        def api_getUsers(self):
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

            return json.dumps(usersData)

        @self.app.route("/addNew")
        def addNew():
            return render_template("addNew.html")

        print("web_Api: OK!")

    def __run(self):
        self.app.run(host=self.host, debug=True)  # , port=self.port, debug=True)

    def run(self):
        print("web_Api: Running...")

        self.appProcess.start()

        print("web_Api: OK!")

    def stop(self):
        print("web_Api: Stopping...")

        self.appProcess.terminate()
        self.appProcess.join()

        print("web_Api: OK!")


if __name__ == "__main__":
    print("Run main.py!")
