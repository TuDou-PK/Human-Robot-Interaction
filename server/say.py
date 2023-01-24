import qi
import argparse
import sys
import time
import os
import time


def say(strsay):
    pip = '127.0.0.1'
    pport = 9559
    language = 'English'
    speed = 100
    session = qi.Session()
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        session.connect(connection_url)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    tts_service = session.service("ALTextToSpeech")

    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)
    tts_service.say(strsay)
    time.sleep(1)

