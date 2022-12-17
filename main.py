import os
import subprocess
import re
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
#sense.low_light=True

#########################################################################################################################
# Uncomment one of the following modes

# Tries to connect the first registered preferredIn to the first registered preferredOut until successful
# mode = 'simple'

# Tries to connect the first registered preferredIn to the first registered preferredOut each time a button is pressed
# mode = 'press'

# Connect all inputs to all outputs every second (probably not a good idea)
# mode = 'frenzy'

# Use a senseHat to manually control midi links (starts in simple mode until button is pressed)
mode = 'senseHat'
#########################################################################################################################


# Hardcode an array of preferred devices here
# Run "aconnect -l" to list device names
preferredIn = ['Arturia MiniLab mkII']
preferredOut = ['UNO Synth']

# Declare the global input and output to be used in any mode
i = ''
o = ''

# Declare the global available inputs and outputs to be used in any mode
allInputs = []
allOutputs = []

def readConnections():
    # Get the system output for device names
    inputString = subprocess.check_output("aconnect -i", shell=True, text=True)
    outputString = subprocess.check_output("aconnect -o", shell=True, text=True)

    # Some regex for getting an array of device names from the full string
    allInputs =  re.findall(r"'([^']*)'", inputString)
    allOutputs = re.findall(r"'([^']*)'", outputString)

    # Ignore some of the default system device names
    deviceNamesToIgnore = ['MIDI', 'Midi', 'System', 'Timer', 'Announce', 'Through']
    for x in deviceNamesToIgnore:
        for y in allInputs[:]:
            if x in y:
                allInputs.remove(y)
        for y in allOutputs[:]:
            if x in y:
                allOutputs.remove(y)

    print(f"Available Inputs: {allInputs}")
    print(f"Available Outputs: {allOutputs}")

def link():
    global i
    global o
    os.system(f"aconnect '{i}' '{o}'")
    print(f"{i} connected to {o}")
    sense.show_message(f"{i} connected to {o}", text_colour=[0,255,255], scroll_speed=0.02)

def setIOToPreferred():
    global i
    global o
    global allInputs
    global allOutputs
    for x in preferredIn:
            if x in allInputs:
                i=x
                break
        for x in preferredOut:
            if x in allOutputs:
                o=x
                break

if mode == 'simple'
    readConnections()
    connected = False
    while connected == False:
        #os.system("aconnect -x")
        global i
        global o
        
        if len(allInputs) == 0:
            print('No Inputs Detected')
            sense.show_message('No Inputs Detected', scroll_speed=0.02)
            return
        if len(allOutputs) == 0:
            print('No Outputs Detected')
            sense.show_message('No Outputs Detected', scroll_speed=0.02)
            return
        
        setIOToPreferred()
        
        if i == '' or o == '':
            print("NICE TRY LOSER")
        else:
            link()
            connected = True


if mode=='senseHat':
    readConnections()

    setIOToPreferred()

    # if preferred connections exist, link them, but still wake up when button pressed
    if i != '' and o != '':
        link()
    
    # position in device arrays to display on the senseHat
    listPosition = 0
    # 0 for selecting input, 1 for selecting output, 2 for sleep
    selecting = 'sleep'
    global i
    global o

    def clamp(value, min_value=0, max_value=len(allInputs)-1):
        return min(max_value, max(min_value, value))

    def pushed_up(event):
        global listPosition
        if event.action != ACTION_RELEASED:
            listPosition = clamp(listPosition - 1)
            sense.clear()

    def pushed_down(event):
        global listPosition
        if event.action != ACTION_RELEASED:
            listPosition = clamp(listPosition + 1)
            sense.clear()

    def pushed_middle(event):
        global listPosition
        global selecting
        global i
        global o
        if event.action != ACTION_RELEASED:
            sense.clear()
            print(selecting)
            if selecting == 'input':
                i = allInputs[listPosition]
                selecting = 'output'
            elif selecting == 'output':
                o = allOutputs[listPosition]
                selecting = 'sleep'
            elif selecting == 'sleep':
                selecting = 'input'
            listPosition = 0
        sense.clear()

    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_middle = pushed_middle

    def loop():
        global i
        global o
        global listPosition
        global selecting
        while True:
            while selecting == 0:
                sense.show_message(allInputs[listPosition], scroll_speed=0.02, text_colour=[0,255,0])
            while selecting == 1:
                sense.show_message(allOutputs[listPosition], scroll_speed=0.02, text_colour=[0,0,255])
            link()
            while selecting == 2:
                # What are you waiting for?
                # I don't know... something awesome I guess
                pass
    loop()
