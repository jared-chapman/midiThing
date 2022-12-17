import os
import subprocess
import re
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
#sense.low_light=True
os.system("aconnect -x")

deviceNamesToIgnore = ['MIDI', 'Midi', 'System', 'Timer', 'Announce', 'Through']
preferredIn = ['Arturia MiniLab mkII']
preferredOut = ['UNO Synth']

inputString = subprocess.check_output("aconnect -i", shell=True, text=True)
outputString = subprocess.check_output("aconnect -o", shell=True, text=True)


allInputs =  re.findall(r"'([^']*)'", inputString)
allOutputs = re.findall(r"'([^']*)'", outputString)


for x in deviceNamesToIgnore:
    for y in allInputs[:]:
        if x in y:
            allInputs.remove(y)
    for y in allOutputs[:]:
        if x in y:
            allOutputs.remove(y)

print(f"IN: {allInputs}")
print(f"OUT: {allOutputs}")
def priorityLink():
    sense.show_message("Running Priority Link", scroll_speed=.02)
    i = ''
    o = ''
    
    if len(allInputs) == 0:
        print('No Inputs Detected')
    if len(allOutputs) == 0:
        print('No Outputs Detected')
    
    for x in preferredIn:
        if x in inputString:
            i=x
            break
    for x in preferredOut:
        if x in outputString:
            o=x
            break
    
    if i == '' or o == '':
        print("NICE TRY LOSER")
    else:
        print(f'Connecting {i} to {o}')
        os.system(f"aconnect '{i}' '{o}'")

listPosition = 0
# 0 for selecting input, 1 for selecting output, 2 for sleep
selecting = 0
i = ''
o = ''
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
        print("middle pressed")
        print(selecting)
        if selecting == 0:
            i = allInputs[listPosition]
            selecting = 1
        elif selecting == 1:
            o = allOutputs[listPosition]
            selecting = 2
        elif selecting == 2:
            selecting = 0
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
        os.system(f"aconnect '{i}' '{o}'")
        sense.show_message(f"{i} connected to {o}", text_colour=[0,255,255], scroll_speed=0.02)
        print(f'Connecting {i} to {o}')
        while selecting == 2:

            #Just wait I guess
            pass

loop()
