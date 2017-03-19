# Code to communicate with divoom devices like Aurabox. #

## Sending pictures to divoom devices ##

### Protocol typical 62 bytes ####
8 bytes PREFIX
50 bytes (clean) DATA
3-4 bytes POSTFIX

#### PREFIX static ####
01 39 00 44 00 0a 0a 04

#### DATA ####
One pixel is represented by half a byte. The lower byte is the the first (left) pixel.
50 bytes are 100 half bytes. Ordered in rows.
There are 8 colors: 0-7 where 0 is black and 7 is white.
Within this data, the invalid bytes procedure is applied as decribed in the text.

#### invalid bytes ####
If some data contains invalid bytes they are masked.
invalid bytes are 0x01, 0x02 and 0x03.
masking procedure is: 
first prepend the byte with another byte (0x03)
then add 0x03 to the invalid byte and append it.
example: original = 0x01 -> corrected 0x03 0x04

#### POSTFIX ####
1. byte lower byte of the SUM over (PREFIX without first byte) + DATA
2. byte upper bytes of the SUM over (PREFIX without first byte) + DATA (invalid bytes
3. byte "03" (seems to only be active if there are no invalid bytes, invalid bytes are 0x01-0x03)
4. byte "02"

## running tests ##
python -m divoom-test