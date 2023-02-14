from helper import *

filename = 's2c10.txt'
file = open(filename,mode='r')
lines = file.read()
encrypted = base64_to_hex(lines)
key = string_to_hex("YELLOW SUBMARINE")
    
print(hex_to_ascii_string(decrypt_AES_CBC(key,encrypted)))
