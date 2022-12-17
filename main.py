import os
import subprocess
import re
os.system("aconnect -x")

deviceNamesToIgnore = ['MIDI', 'Midi', 'System', 'Timer', 'Announce', 'Through']
preferredIn = ['Arturia MiniLab mkII']
preferredOut = ['UNO Synth']

inputString = subprocess.check_output("aconnect -i", shell=True, text=True)
outputString = subprocess.check_output("aconnect -o", shell=True, text=True)


allInputs =  re.findall(r"'([^']*)'", inputString)
allOutputs = re.findall(r"'([^']*)'", outputString)

#for x in allInputs[:]:
    #for y in deviceNamesToIgnore:
        #if y in x:
            #allInputs.remove(x)
            #break

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

priorityLink()
