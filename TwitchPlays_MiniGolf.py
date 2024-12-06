##################### LIBRARY IMPORTS #####################

# General purpose. Not necessarily used yet.
import math
import string
import random

#  Used for mouse movement output.
import pydirectinput
import pyautogui

# Used for keyboard output.
from TwitchPlays_KeyCodes import *



##################### GLOBAL SCRIPT VARIABLES #####################

# Constants, change for different amount of permitted slight adjustments.
MAX_SLIGHT_POWER_COUNT = 3
MAX_SLIGHT_AIM_COUNT = 3

# Used for golf functions.
ADJUSTING_POWER = False
X_VECTOR = 0
Y_VECTOR = 0

SLIGHT_POWER_COUNT = MAX_SLIGHT_POWER_COUNT
SLIGHT_AIM_COUNT = MAX_SLIGHT_AIM_COUNT


##################### SPECIFIC SCRIPT FUNCTIONS #####################



def change_vectors(x_mod,y_mod):
    global X_VECTOR
    global Y_VECTOR
    
    ### Ensures that the changed vector results in the same sign as the nonzero modifier.
    if X_VECTOR * x_mod < 0:
        X_VECTOR = 0
    
    if Y_VECTOR * y_mod < 0:
        Y_VECTOR = 0
    

    X_VECTOR += x_mod
    Y_VECTOR += y_mod



def reset_vectors():
    global X_VECTOR
    global Y_VECTOR

    X_VECTOR = 0
    Y_VECTOR = 0
    


##################### PUBLIC METHODS #####################

# Initialization
def init():
    pyautogui.FAILSAFE = False



def handle_message(orig_msg, orig_user, last_message):

    global ADJUSTING_POWER
    global X_VECTOR
    global Y_VECTOR

    # Used to restrict amount of slight adjustments for balance purposes.
    global SLIGHT_AIM_COUNT
    global SLIGHT_POWER_COUNT

    # Identifies if a command was executed, later returned to main script.
    executed_command = False

    try:

        ### Adjusting message & username for more flexible command matching.

        msg = str.lower(orig_msg)
        msg.translate(str.maketrans('', '', string.punctuation))
        user = str.lower(orig_user)
        

        ###### CHECK MESSAGE AGAINST VIABLE COMMANDS ######

        if msg == "left" and not ADJUSTING_POWER:
            print("moving left")
            change_vectors(-4,0)

            executed_command = True

        if msg == "right" and not ADJUSTING_POWER:
            print("moving right")
            change_vectors(4,0)

            executed_command = True

        if msg in ["slightly left", "sleft"] and not ADJUSTING_POWER and SLIGHT_AIM_COUNT > 0:
            print("moving a little bit left")
            pydirectinput.moveRel(-15,0,relative=True,duration=0.01)
            SLIGHT_AIM_COUNT -= 1

            executed_command = True

        if msg in ["slightly right", "slight"] and not ADJUSTING_POWER and SLIGHT_AIM_COUNT > 0:
            print("moving a little bit right")
            pydirectinput.moveRel(15,0,relative=True,duration=0.01)
            SLIGHT_AIM_COUNT -= 1

            executed_command = True

        if msg == "up" and not ADJUSTING_POWER:
            print("moving up")
            change_vectors(0,2)

            executed_command = True

        if msg == "down" and not ADJUSTING_POWER:
            print("moving down")
            change_vectors(0,-2)

            executed_command = True

        if msg in ["more", "moar"] and ADJUSTING_POWER:
            print("more power")
            change_vectors(0,5)

            executed_command = True

        if msg == "less" and ADJUSTING_POWER:
            print("less power")
            change_vectors(0,-5)

            executed_command = True

        if msg in ["slightly more", "smore"] and ADJUSTING_POWER and SLIGHT_POWER_COUNT > 0:
            print("giving it a bit more power")
            pydirectinput.moveRel(0,15,relative=True,duration=0.01)
            SLIGHT_POWER_COUNT -= 1

            executed_command = True

        if msg in ["slightly less", "sless"] and ADJUSTING_POWER and SLIGHT_POWER_COUNT > 0:
            print("giving it a bit less power")
            pydirectinput.moveRel(0,-15,relative=True,duration=0.01)
            SLIGHT_POWER_COUNT -= 1

            executed_command = True

        if msg in ["stop", "stahp"]:
            print("stopping movement")
            reset_vectors()

            executed_command = True

        if msg == "jump" and ADJUSTING_POWER == False:
            print("jumping")
            HoldAndReleaseKey(J,0.01)

            executed_command = True

        if msg == "target lock" and ADJUSTING_POWER != True:
            print("target locked, now adjusting power")
            reset_vectors()     # Vectors are reset here to prevent aiming from carrying over to power adjustment.
            ADJUSTING_POWER = True
            pydirectinput.mouseDown()   # Left mouse button must be held down to adjust power in "Golf It" and "Golf With Your Friends".

            executed_command = True

        if msg in ["fire", "shoot"] and last_message in ["fire", "shoot"] and ADJUSTING_POWER == True:
            print("firing")
            reset_vectors()     # Vectors are reset here to prevent movement carrying over from power adjustment.
            ADJUSTING_POWER = False
            pydirectinput.mouseUp()     # Left mouse button is released to fire with current power in "Golf It" and "Golf With Your Friends".

            ### Slight adjustment counts reset to allow slight adjustments on following next turn.
            SLIGHT_POWER_COUNT = MAX_SLIGHT_POWER_COUNT
            SLIGHT_AIM_COUNT = MAX_SLIGHT_AIM_COUNT

            executed_command = True
        
        if msg == "aim" and last_message == "aim" and ADJUSTING_POWER == True:
            print("changing aim, no longer adjusting power")
            reset_vectors()     # Vectors are reset here to prevent movement carrying over from power adjustment.
            ADJUSTING_POWER = False
            pydirectinput.moveRel(0,-5000,relative=True,duration=0.01)  # Mouse is moved back a ridiculous amount to prevent any residual power from accidentally firing.
            time.sleep(0.01)    # Prevents camera from being moved by mouse movement due to right-clicking during mouse movement in "Golf It".
            pydirectinput.rightClick()  # Cancels firing in "Golf It" without accidentally firing. 
            pydirectinput.mouseUp()     # Releases left mouse button to allow "target" command to function properly again.
            SLIGHT_POWER_COUNT = MAX_SLIGHT_POWER_COUNT      # Resets only power count to allow slight power changes once aiming is complete again.

            executed_command = True



        ### Used by TwitchPlays_Main to lock out other commands executing due to the same message.

        return executed_command


        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))


def move_mouse():

    if X_VECTOR != 0 or Y_VECTOR != 0:
        pydirectinput.moveRel(X_VECTOR,Y_VECTOR,duration=0.01,relative=True)