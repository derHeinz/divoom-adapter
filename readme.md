# Code to communicate with divoom devices like Aurabox. #

## Features ##
* Show time
* Show temperature
* Send image
* Send animation loops
* Scrolling of images
* Create text image

## Show time ##
Following static byte array can be sent to show time: 01 04 00 45 00 49 00 02

## Show temperature ##
Following static byte array can be sent to show time: 01 04 00 45 03 04 4a 00 02

## Sending image ##

### Protocol typical 62 bytes ####
8 bytes PREFIX
50-100 bytes DATA
3-5 bytes POSTFIX

#### PREFIX (static) ####
01 39 00 44 00 0a 0a 04

#### DATA ####
One pixel is represented by half a byte. The lower byte is the the first (left) pixel.
50 bytes are 100 half bytes. Ordered in rows.
There are 8 colors: 0-7 where 0 is black and 7 is white.
0 = black
1 = red
2 = green
3 = yellow
4 = blue
5 = pink
6 = light blue
7 = white
red, green, blue, orange, light blue, pink, white, black
Within this data, the invalid bytes procedure is applied as decribed in the text.

#### Invalid bytes ####
If some data contains invalid bytes they are masked.
invalid bytes are 0x01, 0x02 and 0x03.
masking procedure is: 
first prepend the byte with another byte (0x03)
then add 0x03 to the invalid byte and append it.
example: original = 0x01 -> corrected 0x03 0x04

#### POSTFIX ####
1. byte lower byte of the SUM over (PREFIX without first byte) + DATA (invalid bytes error correction applies here - so these may be two bytes)
2. byte upper byte of the SUM over (PREFIX without first byte) + DATA (invalid bytes error correction applies here - so these may be two bytes)
4. byte "02"

## Send animation loops ##
Very similar to sending simple images. You just send several packages containing each single images with slightly different header.
However the prefix changes slightly.
The static part looks like this: 3b 00 49 00 0a 0a 04
The next byte is the number of the image in the animation starting with 0. Note that invalid bytes error correction applies here - so there may be two bytes.
The following byte is the time each single image is shown, smaller number means faster.

## Scrolling of images ##
Allows to send images wider than the box can display and scroll them running to the left.

## Create text image ##
Write text into an image that suits to be displayed as single image or via the scoll functionality.

Font used here: http://kottke.org/plus/type/silkscreen/
Created open format using: otf2bdf -p 8 -r 72 -o slkscr.bdf slkscr.ttf
Created PIL like format using: pilfont.py slkscr.bdf

## Running tests ##
python -m divoom_test

## Needed python libraries (install with pip install) ##
bluepy (bluetooth connection)
pillow (python image processing)

