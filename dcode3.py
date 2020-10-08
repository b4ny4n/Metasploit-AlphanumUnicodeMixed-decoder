#!/usr/bin/python3
import string
import sys
import codecs

# UTF-8 encoded bytes of the shellcode
encoded_bytes=""

if len(sys.argv) != 2:
    print("[+] usage: {} hexencodedfile".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as fh:
    encoded_bytes = fh.read().strip().encode('utf8')
l=int(len(encoded_bytes)/2)

decoded_bytes = str()

fho = open(sys.argv[1]+'.decode','wb')
for i in range(l):

    #iterating on even numbers as beginning of the block
    block=encoded_bytes[i*2:i*2+2]

    #returns the Unicode code point and masks by the lower 4 bits
    decoded_byte_low = block[1] & 0x0F

    #block[1]'s Unicode code point, bitshifted 4 bits to the right
    #block[0]'s Unicode code point, masked by the lower 4 bits
    #sum is masked by the lower 4 bits
    decoded_byte_high = ((block[1] >> 4) + (block[0] & 0x0F)) & 0x0F

    #chr() returns the ASCII character associated to the code point
    decoded_byte=decoded_byte_low + (decoded_byte_high <<4)

    decoded_bytes+=chr(decoded_byte)
    fho.write(decoded_byte.to_bytes(1,'little'))

fho.close()
printable_decoded_bytes = ''.join([c for c in decoded_bytes if c in string.printable])

# ASCII display
print("========== ASCII ==========")
print(printable_decoded_bytes)
print("========== /ASCII =========")
print()
print()
# hexadecimal display
print("========== HEX ==========")
for b in decoded_bytes:
    print(f"{ord(b):02X}",end="")
print("")
print("========== /HEX =========")
print()
print("decoded shellcode written to " + sys.argv[1]+'.decode')
