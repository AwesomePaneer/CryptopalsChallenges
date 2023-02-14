from helper import *
import random

key = random_AES_key()

def first_function():
    arr = [
        "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
    ]
    index = random.randint(0,9)
    chosen_string = arr[index]
    message = string_to_hex(chosen_string)
    IV = random_AES_key()
    cipher = encrypt_AES_CBC(key,message,IV)
    return cipher

def second_function(cipher,IV):
    message = decrypt_AES_CBC(key,cipher,IV)
    return check_valid_PKCS7_padding(message)

cipher = first_function()
print(decrypt_AES_CBC(key,cipher[32:],cipher[0:32]))
print(second_function(cipher[32:],cipher[0:32]))
blocks = get_AES_blocks_from_hex(cipher)
IV = blocks[0]
cipher = blocks[1:]

for i in range(0,256):
    hex_int = get_hex_from_int(i)
