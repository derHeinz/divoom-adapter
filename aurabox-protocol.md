# AuraBox Protocol #
The protocol is message based.
Framing is used to separate messages.

## Framing ##
```
| Start of Frame | Escaped Content | End of Frame |
```

The content is encapsulated with a start of frame (01) and an end of frame (02) byte.
The escape character is 03.
Whenever the byte 01, 02 or 03 is in the content, it is replaced with 04, 05 or 06.

A valid message on this layer looks like:
```
01 04 00 32 d2 08 03 04 02
```

The content of the message is:
```
04 00 32 d2 08 01
```

## Message format ##
```
| Length | Command | Data | Checksum |
```

The message starts with the length of the message.
This is the length of the whole message minus the length itself.
The length is 2 bytes, the lower byte is sent first.

The command is 1 byte.

The length of the data depends on the command.

At the end, the 2 byte long sum over the length, command and data is sent.

A valid message on this layer looks like this:
```
04 00 32 d2 08 01
+++++------------- length:     4h
      ++---------- command:   32h
         ++------- data:      d2h
            +++++- checksum: 108h
```

## Response Format ##
On connection, the device says hello with the sequence:
```
00 05 48 45 4c 4c 4f 00
```

On an frame error (wrong checksum, wrong length), the device answers with an error message.
The error message uses the normal framing, but does not follow the message format.
The error message format is:
```
| Request Command | aa | Checksum |
```

A valid error response for the command 32h looks like:
```
32 aa dc 00
++---------- response to command: 32h
   ++------- error
      +++++- checksum:            dch
```

A successfully received message is answered by the device with a message in the same message format as the request.
It answers with the command 4h and the data:
```
| Request Command | 55 | Response Data |
```

The response to the request with the command 32h and data d2h is:
```
32 55 d2
++------- response to command: 32h
   ++---- success
      ++- respopnse data:      d2h
```

The full frame on the wire of the above example is:
```
01 06 00 04 32 55 d2 63 03 04 02
```
