##################### LIBRARY IMPORTS #####################

# General purpose.
import math
import string
import random
import os

# For playing audio.
import pygame

# For creating window to produce audio.
from tkinter import *

# For preventing audio from playing over itself.
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

def play_sound(sound_path, volume = 1):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


##################### GLOBAL SCRIPT VARIABLES #####################




##################### SPECIFIC SOUND FUNCTIONS #####################

def meow(user):

    ## Identifies which "meow" file to play & constructs filename based on random number generation.
    select_meow = random.randint(1,33)
    select_meow = math.floor((select_meow/2))
    meow_name = ".\\sounds\\meow" + str(select_meow) + ".mp3"

    print(user + " says meow! (" + meow_name + ")")
    play_sound(meow_name)
    return



##################### PUBLIC METHODS #####################

def is_playing_sound():
    return pygame.mixer.music.get_busy()

def load_empty():
    if not is_playing_sound():
        pygame.mixer.music.load(".\\sounds\\empty.mp3")

def stop_sound():
    pygame.mixer.music.stop()

def handle_message(orig_msg, orig_user, last_message):

    # Identifies if a command was executed, later returned to main script.
    executed_command = False

    try:

        ### Adjusting message & username for more flexible command matching.

        msg = str.lower(orig_msg)
        msg.translate(str.maketrans('', '', string.punctuation))
        user = str.lower(orig_user)


        ### Prevents cutting off current sound effect & allows messages to be processed if sound effect is over.

        if is_playing_sound():
            print("Sound already playing, new sound will not play until it is complete.")
            return
        else:
            None



        ###### CHECK MESSAGE AGAINST VIABLE COMMANDS ######

        if msg in ["meow", "mrow", "mrowr"] and not last_message in ["meow", "mrow", "mrowr"]:
            meow(orig_user)
            executed_command = True


        if msg in ["bonk", "bap"] and not last_message in ["bonk", "bap"]:
            play_sound(".\\sounds\\bonk.mp3")



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