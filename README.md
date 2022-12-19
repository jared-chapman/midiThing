# midiThing

## Setup
1. Connect any midi devices you might want to use to a computer
2. Run `aconnect -l` and note the device names (or get their exact midi device name somewhere else I guess)
3. Edit the `preferredInputs` and `preferredOutputs` arrays to include your devices
4. Do something to run `main.py` on startup (crontab, etc.) so we can throw away all monitors, keyboards, and mice

### Simple mode
Simple mode will try to connect the first available preferred input to the first available preferred output, and will keep trying until it connects. 
If a device is unplugged after it is connected it will no reconnect, so if you have a breadboard and some wire you might enjoy...

### Button mode
Run simple mode every time a button is pressed

### Frenzy mode
Connects every available input to every available output every few seconds. Bad idea? 🤷‍♂️

### SenseHat mode
Runs simple mode once to try to connect preferred devices, then uses the [Raspberry Pi SenseHat](https://www.adafruit.com/product/2738) to manually make connections.
1. Press the joystick middle button to start
2. Inputs are displayed in green. Press up and down joystick to move between them, Center button to confirm
3. Outputs are displayed in blue. Press up and down joystick to move between them, Center button to confirm
4. Teal confirmation message shows connection
5. Make all the connections you want!
