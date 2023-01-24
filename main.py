# -*- coding: utf-8 -*-
from __future__ import print_function
import qi
import argparse
import time
import re
import sys
import os
import requests

from gestures import Gesture
from gestures import Vision

from bs4 import BeautifulSoup
from mtranslate import translate




global session
global doGesture


doGesture = True

global text

def main(session, args):
    print("Hello, nice to meet you! I'm pepper.")
    tts_service.say("Hello, nice to meet you! I'm pepper.")
    gesture.doHello()
    stop_flag = False

    # lastInput = ALMemory.subscriber("Dialog/LastInput")
    # print(lastInput.signal)
    #lastInput.signal.connect(dialog)

    while not stop_flag:
        print("What do you want? You can choose to talk, translation, wiki, dance in dialog.")
        print("Or you can do the interaction, touch head, touch hand.")
        mod = raw_input("Please choose: head, hand, dance: ")
        word = mod

        if word == 'exit':
            stop_flag = True

        if word == 'head':
            gesture.touch_head()
            tts_service.say("???")

        if word == 'hand':
            gesture.touch_hand()
            tts_service.say("???")

        if word == 'dance':
            gesture.dance_0()
            audio_player_service.playFile("home/kantsen/playground/Pepper-Interaction/project-pepper/mytest/pop.wav", _async=True)

    print("Byebye")



def dialog_0(lastInput):
    text = lastInput.lower()
    print("text:", text)
    word = text.split(':')
    if 'talk' in word[0]:
        talk = word[1]
        talk = translate(talk, 'zh-CN')
        # print( 'Trans: ', talk)
        res = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        res = res.json()
        strsay = res['content']
        strsay1 = translate(strsay.encode('utf-8'), 'en')
        gesture.look_hand()
        tts_service.say(strsay1)

        print( "Robot: "+strsay1)
    if 'translation'in word[0]:
        gesture.look_hand()
        talk = word[1]
        trans = translate(talk, 'it')
        tts_service.say(trans)
        print('Robot: ', trans)


    if word[0]=='wiki':
        gesture.look_hand()
        talk = word[1]
        url = 'https://en.wikipedia.org/wiki/' + talk.replace(' ', '_')
        web = requests.get(url)
        soup = BeautifulSoup(web.content,'lxml')
        find_all = soup.find_all('p')
   
        rule = re.compile('<[^>]*>|\n\n|\[|\]|, ')
        abstrict = rule.sub('',str(find_all[1:2]))
        abst = abstrict.split('.')
        for a in abst:
            if a == '\n':
                continue
            tts_service.say(rule.sub('', a))
            print( "Robot: "+rule.sub('', a))

    if 'dance' in word[0]:
            audio_player_service.playFile("/home/kantsen/playground/Pepper-Interaction/project-pepper/mytest/pop.wav", _async=True)
            gesture.dance_0()
            

def dialog_1(lastAnswer):
    text = lastAnswer.lower()
    print(lastAnswer.lower())





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")
    
    parser.add_argument("--action", type=str, default='hello',
                        help="port number, the default value is OK in most cases")
    
    parser.add_argument("--sentence", type=str, default="hello",
                        help="Sentence to say")
    parser.add_argument("--language", type=str, default="English",
                        help="language")
    parser.add_argument("--speed", type=int, default=400,
                        help="speed")
    

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://{}:{}".format(args.ip, args.port))
    except RuntimeError:
        print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
               " Run with -h option for help.\n".format(args.ip, args.port))
        sys.exit(1)

    strsay = args.sentence
    language = args.language
    speed = args.speed
    
    tts_service = session.service("ALTextToSpeech")
    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)


    ALDialog = session.service('ALDialog')
    ALMemory = session.service('ALMemory')
    ALMotion = session.service("ALMotion")
    tts_service = session.service("ALTextToSpeech")
    audio_player_service = session.service("ALAudioPlayer")

    # Setup ALDialog
    ALDialog.setLanguage('English')
    vision = Vision()
    gesture = Gesture(ALMotion, doGesture, vision, tts_service, )
    # Start dialog
    ALDialog.subscribe('pepper')
    lastInput = ALMemory.subscriber("Dialog/LastInput")
    lastInput.signal.connect(dialog_0)

    # lastAnswer = ALMemory.subscriber("Dialog/LastAnswer")
    # lastAnswer.signal.connect(dialog_1)
    main(session,args)
