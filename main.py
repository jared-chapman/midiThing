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
#mode = 'simple'

# Tries to connect the first registered preferredIn to the first registered preferredOut each time a button is pressed
# mode = 'press'

# Connect all inputs to all outputs every five seconds (probably not a good idea)
# mode = 'frenzy'

# Use a senseHat to manually control midi links (starts in simple mode until button is pressed)
mode = 'senseHat'
#########################################################################################################################


# Hardcode an array of preferred devices here
# Run "aconnect -l" to list device names
preferredIn = ['Arturia MiniLab mkII']
preferredOut = ['UNO Synth']

deviceNamesToIgnore = ['MIDI', 'Midi', 'System', 'Timer', 'Announce', 'Through']

def getInputs():
    inputString = subprocess.check_output("aconnect -i", shell=True, text=True)
    array = convertDeviceStringToFilteredArray(inputString)
    print(f"All Inputs: {array}")
    return array

def getOutputs():
    outputString = subprocess.check_output("aconnect -o", shell=True, text=True)
    array = convertDeviceStringToFilteredArray(outputString)
    print(f"All Outputs: {array}")
    return array

def convertDeviceStringToFilteredArray(string):
    global deviceNamesToIgnore
    deviceArray =  re.findall(r"'([^']*)'", string)
    for x in deviceNamesToIgnore:
        for y in deviceArray[:]:
            if x in y:
                deviceArray.remove(y)
    return deviceArray

def log(message, color=[255,255,255]):
    print(message)
    if mode == 'senseHat':
        sense.show_message(message, text_colour=color, scroll_speed=0.02)


def link(i, o):
    # Link an input and output, log to terminal and sensehat
    if i != '' and o != '':
        os.system(f"aconnect '{i}' '{o}'")
        message = f"{i} connected to {o}"
        log(message, [0, 255, 255])

def linkIOPreferred():
    global preferredIn
    global preferredOut
    i = ''
    o = ''
    inputs = getInputs()
    outputs = getOutputs()
    for x in preferredIn:
        if x in inputs:
            i=x
            break
    for x in preferredOut:
        if x in outputs:
            o=x
            break
    if i != '' and o != '':
        link(i, o)
        return True
    else:
        return False

if mode == 'simple':
    connected = False
    while connected == False:
        print("1")
        connected = linkIOPreferred()
        time.sleep(1)

if mode == 'frenzy':
    while True:
        inputs = getInputs()
        outputs = getOutputs()
        for x in inputs:
            for y in outputs:
                link(x, y)
        sleep(5)


if mode=='senseHat':
    #########################################################################################################################
    inputColor = [0, 255, 0]
    outputColor = [0, 0, 255]
    confirmColor = [0, 255, 255]
    #########################################################################################################################
    
    linkIOPreferred()

    # position in device arrays to display on the senseHat
    listPosition = 0
    # 0 for selecting input, 1 for selecting output, 2 for sleep
    selecting = 'sleep'
    i = ''
    o = ''
    inputs = getInputs()
    outputs = getOutputs()

    def clamp(value):
        minValue = 0
        maxValue = len(inputs)-1
        if selecting == 'output':
            maxValue = len(outputs)-1
        return min(maxValue, max(minValue, value))

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
                i = inputs[listPosition]
                selecting = 'output'
            elif selecting == 'output':
                o = outputs[listPosition]
                selecting = 'sleep'
            elif selecting == 'sleep':
                selecting = 'input'
            listPosition = 0
        sense.clear()

    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_middle = pushed_middle


    while True:
        while selecting == 'input':
            sense.show_message(inputs[listPosition], scroll_speed=0.02, text_colour=[0,255,0])
        while selecting == 'output':
            sense.show_message(outputs[listPosition], scroll_speed=0.02, text_colour=[0,0,255])
        link(i, o)
        while selecting == 'sleep':
            # What are you waiting for?
            # I don't know... something awesome I guess
            pass

