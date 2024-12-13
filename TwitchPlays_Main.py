##################### LIBRARY IMPORTS #####################

# General purpose.
import math
import string
import random
import time

# Required for Twitch Plays.
import concurrent.futures
import TwitchPlays_Connection

# Required for user keyboard input mid-program.
import keyboard

# Scripts for specific games & other functions.
import TwitchPlays_Audio as Audio_Handler
import TwitchPlays_RainWorld as RainWorld_Handler
import TwitchPlays_MiniGolf as MiniGolf_Handler
import TwitchPlays_TTS as TTS_Handler


##################### GAME VARIABLES #####################

# Replace this with your Twitch username. Must be all lowercase.
TWITCH_CHANNEL = 'skyewint' 

# If streaming on Youtube, set this to False
STREAMING_ON_TWITCH = True

# If you're streaming on Youtube, replace this with your Youtube's Channel ID
# Find this by clicking your Youtube profile pic -> Settings -> Advanced Settings
YOUTUBE_CHANNEL_ID = "YOUTUBE_CHANNEL_ID_HERE" 

# If you're using an Unlisted stream to test on Youtube, replace "None" below with your stream's URL in quotes.
# Otherwise you can leave this as "None"
YOUTUBE_STREAM_URL = None

##################### MESSAGE QUEUE VARIABLES #####################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []


##################### GLOBAL SCRIPT VARIABLES #####################

PAUSED = False
LAST_MESSAGE = ""

# Constants or set during initialization.
Audio_Mode_Active = False
TTS_Mode_Active = False
Game_Modes = ["nothing","minigolf","rain_world"]
Current_Game = 0


##################### INITIALIZATION #####################

while True:
    print("Do you want sound effects turned on? [y]/n")
    selection = input()
    if selection.lower() == "n":
        Audio_Mode_Active = False
        print("Sound effects will be turned off.\n\n")
        break
    else:
        Audio_Mode_Active = True
        Audio_Handler.init()
        print("Sound effects will be turned on.\n\n")
        break

print("\n\n")

while True:
    print("Do you want TTS turned on? [y]/n")
    selection = input()
    if selection.lower() == "n":
        TTS_Mode_Active = False
        print("TTS will be turned off.\n\n")
        break
    else:
        TTS_Mode_Active = True
        if not Audio_Mode_Active:
            Audio_Handler.init()
        TTS_Handler.init()
        print("TTS will be turned on.\n\n")
        break

print("\n\n")
 
while True:
    print("What game are we playing today?")
    print("[0] = No game.")
    print("1 = Mini Golf")
    print("2 = Rain World")

    selection = input()
    try:
        int(selection)
    except:
        Current_game = 0
        break
    else:
        if int(selection) <= len(Game_Modes):
            Current_Game = int(selection)
            break
    
    
    ## If selection does not exist in the possible game modes, request input again.
    print("Invalid response.\n\n")

print("\n\n")
print("Press q to initiate script.")
keyboard.wait("q")



##################### Initiating Connection #####################

if STREAMING_ON_TWITCH:
    t = TwitchPlays_Connection.Twitch()
    t.twitch_connect(TWITCH_CHANNEL)
else:
    t = TwitchPlays_Connection.YouTube()
    t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)



##################### GENERAL METHODS #####################

def handle_message(message):

    # Updated by function after being passed to commands. Not for use in other scripts.
    global LAST_MESSAGE


    # If a message is processed as a valid command, commands_locked prevents unwanted additional effects.
    commands_locked = False


    try:
        msg = message['message']
        username = message['username']

        print("Got this message from " + username + ": " + msg)



        if Game_Modes[Current_Game] == "minigolf" and not commands_locked and not PAUSED:

            commands_locked = MiniGolf_Handler.handle_message(msg, username, LAST_MESSAGE)

        elif Game_Modes[Current_Game] == "rain_world" and not commands_locked and not PAUSED:

            commands_locked = RainWorld_Handler.handle_message(msg, username, LAST_MESSAGE)


        ### Separated from game modes to prevent multiple effects on one command.
        if Audio_Mode_Active and not commands_locked:
            commands_locked = Audio_Handler.handle_message(msg, username, LAST_MESSAGE)

        if TTS_Mode_Active and not commands_locked:
            TTS_Handler.handle_message(msg, username)


        LAST_MESSAGE = msg


        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))



##################### MAIN LOOP #####################

while True:

    if not PAUSED and Game_Modes[Current_Game] == "minigolf":
        MiniGolf_Handler.move_mouse()
        
    if Audio_Mode_Active or TTS_Mode_Active:
        Audio_Handler.update()


    ##################### MESSAGE HANDLING #####################

    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages();
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages


    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time();


    ##################### USER INPUT HANDLING #####################

    # If user presses Shift+P, ignore all messages until "q" is pressed.
    if keyboard.is_pressed('shift+p') and not PAUSED:
        print("Please press q to continue.")
        PAUSED = True

    if keyboard.is_pressed('q') and PAUSED:
        print("Continuing.")
        PAUSED = False

    if keyboard.is_pressed('backspace'):
        Audio_Handler.stop_sound()


    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        if TTS_Mode_Active:
            TTS_Handler.quit()
        if Audio_Mode_Active or TTS_Mode_Active:
            Audio_Handler.quit()
        exit()


    ##################### MESSAGE HANDLING 2 q#####################

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')


    time.sleep(0.005)
    


###
# Set up a queue system so text to speech messages aren't lost, generally.