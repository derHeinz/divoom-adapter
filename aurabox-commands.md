# AuraBox Commands #

## Set Brightness ##

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     32h |              1 |               1 |

The request data can be one of:

| value | brightness |
| -----:| ---------- |
|    0h | off        |
|   3fh | dark       |
|   d2h | light      |

The response data is the same as sent in the request.


## Switch Screen ##

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     45h |              1 |               1 |

The request data can be one of:

| value | screen                             |
| -----:| ---------------------------------- |
|     0 | time                               |
|     1 | temperature                        |
|     2 | light                              |
|     3 | equalizer                          |
|     4 | discover the boundless imagination |
|     5 | party rock                         |
|     6 | soar to the rainbow                |
|     7 | fuel the stellar explosion         |

The response data is the same as sent in the request.


## Set Time ##

Shown on [screen](#switch-screen) 0, time.

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     18h |              8 |               0 |

Request data:

| Position | Description                                  |
| --------:| -------------------------------------------- |
|        0 | last 2 digits of the year (i.e. 18 for 2018) |
|        1 | first 2 digits of the year (i.e. 20)         |
|        2 | month, starting with January = 0             |
|        3 | day of the month, starting with 1            |
|        4 | hour                                         |
|        5 | minute                                       |
|        6 | second                                       |
|        7 | day of week, starting with Sunday = 1        |

It seems that only the hour, minute and seconds are used by the device.


## Set Temperature Unit ##

Shown on [screen](#switch-screen) 1, temperature.

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     4ch |              1 |               1 |

The request data can be one of:

| value | unit      |
| -----:| --------- |
|     0 | Celsius   |
|     1 | Farenheit |

The response data is the same as sent in the request.


## Set Color ##

Shown on [screen](#switch-screen) 2, light.

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     47h |              1 |               1 |

The request data is a color value.
A color value are 3 bits for the colors red (bit 0), green (bit 1) and blue (bit 2).
This gives the colors:

| value | color     |
| -----:| --------- |
|     0 | black     |
|     1 | red       |
|     2 | green     |
|     3 | orange    |
|     4 | blue      |
|     5 | purple    |
|     6 | cyan      |
|     7 | white     |

The response data is the same as sent in the request.


## Show Image ##

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     44h |             54 |               1 |

The data is made of the image header and the image data.
The image header is `00 10 10 04` and not used by the device.

The image data are the pixels from top left to the bottom right, ordered in rows.
One pixel is represented by half a byte, colors are the same as described in [Set Color](#set-color).
2 pixels are sent in one byte, the first pixel in the lower nibble.

The response data is 0.


## Show Animation ##

| Command | Request length | Response length |
| -------:| --------------:| ---------------:|
|     49h |             56 |               1 |

The data is made of the image header, the animation header and the image data.
The image header is the same as in [Show Image](#show-image).

The animation header is 2 bytes, the frame number and the frame duration.
Animation frames have to be sent one after the other, from frame number 0 to the highest frame number (7 or less).
The frame is show for about 0.2 + `frame duration` * 0.1 seconds.

The image data is the same as in [Show Image](#show-image).

The response data is 1.
