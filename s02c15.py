from helper import *

string = "ICE ICE BABY\x04\x04\x04\x04"
hex_string = string_to_hex(string)
print(check_valid_PKCS7_padding(hex_string))