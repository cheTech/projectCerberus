""" 
Cerberus App main class.

Author: cheTech
GitHub: https://github.com/cheTech/projectCerberus

Documentation: 
"""
from texttospeechApi import texttospeech_Api
from databaseApi import database_Api
from identifyApi import identify_Api
from webApi import web_Api
import logging


class CerberusApplication(object):

    def __init__(self, settings):
        print("CerberusApplication: Started init...")

        handler = logging.FileHandler("project.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.db = database_Api(settings["Database Credentials"])

        self.tts = texttospeech_Api(settings["texttospeech Keys"])

        self.identify = identify_Api(dbObj=self.db, ttsObj=self.tts, identifyOptions=settings["Identify Settings"])
        self.web = web_Api(settings["Web Api Settings"], dbObj=self.db, handler=handler)

        print("CerberusApplication: OK!")

    def run(self):
        print("CerberusApplication: Running...")

        self.web.run()
        self.tts.run()
        self.identify.run()

        print("CerberusApplication: OK!")

        while True:
            open("CerberusProjectStatus.txt", "r").read()
            if open("CerberusProjectStatus.txt", "r").read() == "0":
                self.stop()
                break

    def stop(self):
        print()
        print("CerberusApplication: Stopping...")

        self.web.stop()
        self.tts.stop()
        self.identify.stop()

        print("CerberusApplication: OK!")


if __name__ == "__main__":
    print("Run main.py!")
