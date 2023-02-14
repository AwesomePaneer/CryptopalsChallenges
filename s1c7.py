from helper import *

filename = 's1c7.txt'
file = open(filename,mode='r')
lines = file.read()
encrypted = base64_to_hex(lines)

key = 'YELLOW SUBMARINE'
hex_key = string_to_hex(key)

print(hex_to_ascii_string(decrypt_AES_ECB(hex_key, encrypted)))
    