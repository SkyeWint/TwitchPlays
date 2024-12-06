##################### LIBRARY IMPORTS #####################

# General purpose.
import math
import string
import random
import re
import time
import os

# Generating TTS files.
from gtts import gTTS

# For playing TTS once it is generated.
import TwitchPlays_Audio as Audio_Handler

##################### GENERAL PURPOSE FUNCTIONS #####################



##################### GLOBAL SCRIPT VARIABLES #####################


# Used to prevent the same user from saying a message twice in a row (if desired).
LAST_USER = ""


##################### PUBLIC METHODS #####################



def handle_message(orig_msg, orig_user):


    # Identifies if a command was executed, later returned to main script.
    executed_command = False

    try:

        verification = str.lower(orig_msg)
        verification.translate(str.maketrans('', '', string.punctuation))
        user = str.lower(orig_user)
        verification.startswith('tts ')

        if Audio_Handler.is_playing_sound():
            print("TTS already happening, cancelling.")
            return
        elif not verification.startswith('tts '):
            print("Not a tts message.")
            return
        #elif LAST_USER == user:
        #    print("This person talked last time, give somebody else a turn!")
        #    return
        else:
            LAST_SOUND_DURATION = 0

        msg = orig_msg[4:]

        Audio_Handler.load_empty()

        if os.path.isfile(".\\sounds\\speech.mp3"):
            os.remove(".\\sounds\\speech.mp3")

        speech = gTTS(text = msg, lang = "en", slow = False)

        speech.save(".\\sounds\\speech.mp3")

        Audio_Handler.play_sound(".\\sounds\\speech.mp3")

        LAST_USER = user


        ### Identifies when the last TTS was generated to prevent overwriting.
        LAST_SOUND_TIME = time.monotonic()

        return

        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))
