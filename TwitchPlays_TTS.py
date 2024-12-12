##################### LIBRARY IMPORTS #####################

# General purpose.
import math
import string
import random
import re
import time
import os
import queue

# Generating TTS files.
from gtts import gTTS

# Currently broken
# from pydub import AudioSegment

import pyttsx3


# For playing TTS once it is generated.
import TwitchPlays_Audio as Audio_Handler

##################### GENERAL PURPOSE FUNCTIONS #####################

MESSAGE_QUEUE = queue.Queue(0)

pyTTS = None
pyTTS_RATE = 200
pyTTS_BASERATE = 200

def init():
    global pyTTS
    global pyTTS_voices

    pyTTS = pyttsx3.init()

### Currently broken due to pydub being broken
""" def mp3_to_wav(orig, target):
    None """

def generate_gTTS(msg, slow = False, filename = "speech"):

    file = ".\\sounds\\" + filename + ".mp3"

    speech = gTTS(text = msg, lang = "en", slow = False)
    speech.save(file)

    return file

def generate_pyTTS(msg, voice = random.randint(0,1), rate = 200, filename = "speech"):
    pyTTS_voices = pyTTS.getProperty('voices')
    file = ".\\sounds\\" + filename + ".wav"

    pyTTS.setProperty("voice", pyTTS_voices[voice].id)
    pyTTS.setProperty("rate", rate)
    pyTTS.save_to_file(msg, file)

    # The following line actually generates the file, save_to_file only queues TTS to be generated.
    pyTTS.runAndWait()

    return file

def clear_speech_files():
    Audio_Handler.load_empty()

    if os.path.isfile(".\\sounds\\speech.wav"):
        os.remove(".\\sounds\\speech.wav")

    if os.path.isfile(".\\sounds\\speech.mp3"):
        os.remove(".\\sounds\\speech.mp3")


##################### GLOBAL SCRIPT VARIABLES #####################


# Used to prevent the same user from saying a message twice in a row (if desired).
LAST_USER = ""


##################### PUBLIC METHODS #####################



def handle_message(orig_msg, orig_user):


    # Identifies if a command was executed, later returned to main script.
    executed_command = False

    try:

        verification = str.lower(orig_msg)
        user = str.lower(orig_user)

        if not verification.startswith('[tts] '):
            print("Not a tts message.")
            return

        # Gets rid of the "[tts] " to prevent it from being read out loud.
        msg = orig_msg[6:]

        MESSAGE_QUEUE.put(msg)


        return

        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))



def next_TTS_message(): # Creates TTS file and returns the relative file path.

    tts_file = None
    messages_left = MESSAGE_QUEUE.qsize()

    try:
        msg = MESSAGE_QUEUE.get()

    except queue.Empty:
        print(queue.Empty)
    
    else: 
        clear_speech_files()
        
        rate = int((math.sqrt(messages_left) + 0.5) * 200)
    
        voice_selector = str.lower(msg)

        if voice_selector.startswith('[m] '):
            msg = msg[4:]
            tts_file = generate_pyTTS(msg, voice = 0, rate = rate)

        elif voice_selector.startswith('[f] '):
            msg = msg[4:]
            tts_file = generate_pyTTS(msg, voice = 1, rate = rate)

        elif voice_selector.startswith('[g] '):
            msg = msg[4:]
            tts_file = generate_gTTS(msg)

        else: 
            tts_type = random.randint(0, 2)
            if tts_type == 0 or tts_type == 1:
                tts_file = generate_pyTTS(msg, voice = tts_type, rate = rate)
            elif tts_type == 2:
                tts_file = generate_gTTS(msg)

    return tts_file



def message_in_queue():
    return not MESSAGE_QUEUE.empty()
    


def quit():

    MESSAGE_QUEUE.shutdown(True)

    clear_speech_files()