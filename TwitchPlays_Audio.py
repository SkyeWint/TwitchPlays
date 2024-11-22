##################### LIBRARY IMPORTS #####################

# General purpose.
import math
import string
import random

# For playing audio.
import pygame

# For creating window to produce audio.
from tkinter import *

# For identifying audio file length and sleeping until done.
from mutagen.mp3 import MP3
import time



##################### GENERAL PURPOSE DEFINITIONS & INITIALIZATION #####################


## Initializing pygame audio mixer and tkinter window for playback.

ROOT = None
LABEL = None

def init():
    global ROOT
    global LABEL

    pygame.mixer.init()
    ROOT = Tk()
    LABEL = Label(ROOT, text="Hi chat!")
    LABEL.pack()

## Defining general use functions.

def play_sound(sound_path):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()


def get_duration(audio_name):
    audio = MP3(audio_name)
    return audio.info.length



##################### GLOBAL SCRIPT VARIABLES #####################

LAST_SOUND_TIME = 0
LAST_SOUND_DURATION = 0



##################### SPECIFIC SOUND FUNCTIONS #####################

def meow(user):

    ## Identifies which "meow" file to play & constructs filename based on random number generation.
    select_meow = random.randint(1,17)
    select_meow = math.floor((select_meow/2))
    meow_name = "meow" + str(select_meow) + ".mp3"

    print(user + " says meow! (" + meow_name + ")")
    play_sound(meow_name)
    return get_duration(meow_name)



##################### PUBLIC METHODS #####################

def handle_message(orig_msg, orig_user, last_message):

    global LAST_SOUND_TIME
    global LAST_SOUND_DURATION

    # Identifies if a command was executed, later returned to main script.
    executed_command = False

    try:

        ### Adjusting message & username for more flexible command matching.

        msg = str.lower(orig_msg)
        msg.translate(str.maketrans('', '', string.punctuation))
        user = str.lower(orig_user)


        ### Prevents cutting off current sound effect & allows messages to be processed if sound effect is over.

        if time.monotonic() - LAST_SOUND_TIME < LAST_SOUND_DURATION:
            print("Currently playing sound.")
            return
        else:
            LAST_SOUND_DURATION = 0



        ###### CHECK MESSAGE AGAINST VIABLE COMMANDS ######

        if msg in ["meow", "mrow", "mrowr"] and not last_message in ["meow", "mrow", "mrowr"]:
            LAST_SOUND_DURATION = meow(orig_user)
            executed_command = True
        else:
            print("Invalid or repeat command.")






        ### Identifying when the last valid sound effect was played to prevent cutting off current sound.

        LAST_SOUND_TIME = time.monotonic()


        ### Used by TwitchPlays_Main to lock out other commands executing due to the same message.
        
        return executed_command


        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))


def update():

    ROOT.update()


def quit():

    ROOT.quit()