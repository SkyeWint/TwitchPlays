##################### LIBRARY IMPORTS #####################

# General purpose.
import random
import string

# For keyboard output.
from TwitchPlays_KeyCodes import *



##################### GLOBAL SCRIPT VARIABLES #####################

None



##################### SPECIFIC SCRIPT FUNCTIONS #####################

def meow(user):
    
    meow_length = random.uniform(0.05, 1.0)
    HoldAndReleaseKey(M, meow_length)
    print(user + " meowed for " + meow_length + " seconds")



##################### PUBLIC METHODS #####################

def handle_message(orig_msg, orig_user, last_message):


    # Identifies if a chat message resulted in a command being executed; later returned to main script.
    executed_command = False

    try:
        
        ### Adjusting message & username for more flexible command matching.

        msg = str.lower(orig_msg)
        msg.translate(str.maketrans('', '', string.punctuation))
        user = str.lower(orig_user)

        

        ###### CHECK MESSAGE AGAINST VIABLE COMMANDS ######

        if msg in ["meow", "mrow", "mrowr"] and not last_message in ["meow", "mrow", "mrowr"]: 
            meow()
            executed_command = True
        else:
            print("Invalid or repeat command.")



        ### Used by TwitchPlays_Main to lock out other commands executing due to the same message.
        
        return executed_command


        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))