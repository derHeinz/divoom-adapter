# Code to communicate with divoom devices like Aurabox. #

## Features ##
* Show time
* Set time
* Show temperature
* Send image
* Send animation loops
* Scrolling of images
* Create text image
* 3 brightness modes (light, dark, off)

For detailed information about the protocol, see the [AuraBox Protocol](aurabox-protocol.md).
All details about the AuraBox native commands are in the full list of the [AuraBox Commands](aurabox-commands.md).

## Scrolling of images ##
Allows to send images wider than the box can display and scroll them running to the left.

## Create text image ##
Write text into an image that suits to be displayed as single image or via the scoll functionality.

Font used here: http://kottke.org/plus/type/silkscreen/
Created open format using: otf2bdf -p 8 -r 72 -o slkscr.bdf slkscr.ttf
Created PIL like format using: pilfont.py slkscr.bdf

## Running tests ##
```sh
python -m unittest discover -p '*_test.py'
```

## Needed python libraries (install with pip install) ##
* pybluez (bluetooth connection) you probably need to install other things: sudo apt-get install libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev
* pillow (python image processing)

## Running the examples ##
```sh
python show-time.py 01:23:45:67:89:AB
python example.py 01:23:45:67:89:AB
```
