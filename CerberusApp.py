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


class CerberusApplication(object):

    def __init__(self, settings):
        print("CerberusApplication: Started init...")

        self.db = database_Api(settings["Database Credentials"])

        self.face_encodings = self.db.getEncodings()
        self.face_names = self.db.getNames()

        self.tts = texttospeech_Api(settings["texttospeech Keys"])

        self.identify = identify_Api(people_data=[self.face_names,
                                                  self.face_encodings], ttsObj=self.tts, identifyOptions=settings["Identify Settings"])
        self.web = web_Api(settings["Web Api Settings"], dbObj=self.db)

        print("CerberusApplication: OK!")

    def run(self):
        print("CerberusApplication: Running...")

        self.web.run()
        self.identify.run()
        self.tts.run()

        print("CerberusApplication: OK!")

        while True:
            if not self.identify.identifyActive:
                self.stop()
                break

    def stop(self):
        print()
        print("CerberusApplication: Stopping...")

        self.web.stop()
        self.identify.stop()
        self.tts.stop()

        print("CerberusApplication: OK!")


if __name__ == "__main__":
    print("Run main.py!")
