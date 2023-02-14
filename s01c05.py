from helper import *

str = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
multiplier = len(str)//3 + 1
key = ("ICE" * multiplier)[:len(str)]

hex_str = string_to_hex(str)
hex_key = string_to_hex(key)
print(xor_2_hex_strings(hex_str,hex_key))