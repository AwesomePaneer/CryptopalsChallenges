import base64
from itertools import combinations
from random import randbytes
from Crypto.Cipher import AES

def xor_2_hex_strings(s1, s2):
    # s=""
    # for i in range(min(len(s1),len(s2))):
    #     c1 = int(s1[i],16)
    #     c2 = int(s2[i],16)
    #     c = c1^c2
    #     s+=str(c)
    # return s
    #------------------------------------------------
    # s1 = bytes.fromhex(s1).decode('ascii')
    # s2 = bytes.fromhex(s2).decode('ascii')
    # s = "".join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))
    # return s.encode('ascii').hex()
    #------------------------------------------------
    # s = "".join(str(int(x,16) ^ int(y,16)) for x, y in zip(s1, s2))
    # return s
    #------------------------------------------------
    s = "".join('{:x}'.format(int(x,16)^int(y,16)) for x, y in zip(s1, s2))
    return s

def hex_to_ascii_string(hex):
    return bytes.fromhex(hex).decode('ascii')

def hex_to_utf8_string(hex):
    return bytes.fromhex(hex).decode('utf-8')

def string_to_hex(str):
    return str.encode('ascii').hex()

def string_to_binary_string(s):
    binary = ""
    for c in s:
        to_add = str(int(bin(ord(c))[2:]))
        while not len(to_add) == 8:
            to_add = '0'+to_add
        binary += to_add
    return binary

def hamming_distance(s1,s2):    #assuming len(s1) == len(s2)
    s1 = string_to_binary_string(s1)
    s2 = string_to_binary_string(s2)
    distance = 0
    for i in range(0,len(s1)):
        if(s1[i]!=s2[i]):
            distance+=1
    return distance

def check_valid_PKCS7_padding(string):  #string in hex
    last_byte = string[-2:]
    last_byte_int = int(last_byte,16)
    index = len(string) - 2
    check = True
    for i in range(0,last_byte_int):
        if not string[index:index+2] == last_byte:
            check = False
        index -= 2
    return check

def remove_valid_PKCS7_padding(hex_string):
    if check_valid_PKCS7_padding(hex_string):
        last_byte = hex_string[-2:]
        last_byte_int = int(last_byte,16)
        hex_string = hex_string[0:len(hex_string)-2*last_byte_int]
    return hex_string

def nCr_combinations(arr,r):
    return list(combinations(arr,r))

def hex_to_base64(hex):
    return base64.b64encode(bytearray.fromhex(hex)).decode('utf-8')

def bytes_to_utf8_string(b):
    return b.decode('utf-8')

def utf8_string_to_bytes(str):
    return bytes(str,'utf-8')

def hex_to_bytes(hex):
    return bytes.fromhex(hex)

def get_hex_from_int(i):    #int in [0,255]
    h = str(hex(i))[2:]
    if len(h)%2 == 1:
        h = '0' + h
    return h

def base64_to_hex(base64_str):
    return base64.b64decode(base64_str).hex()

def is_ascii_printable(s):    # returns true if it contains ascii printable characters
    # return all(ord(c) <= 127 and ord(c) >=32 for c in s)
    return all((ord(c) <= 127 and ord(c)>=32) or ord(c) in [10] for c in s)

def is_ascii_english(s):    # [A-Z,a-z,0-9,space,newline]
    return all((ord(c) <= 90 and ord(c)>=65) or (ord(c) <= 122 and ord(c)>=97) or (ord(c) <= 57 and ord(c)>=48) or ord(c) in [10,32,] for c in s)

# def get_xored_array_for_single_character_xor(s,start_ascii,end_ascii):
#     arr = []
#     for i in range(start_ascii,end_ascii):
#         char_hex_string = hex(i)[2:] * (int)(len(s)/2)
#         xored_string = xor_2_hex_strings(s,char_hex_string)
#         arr.append(xored_string)
#     return arr

def pad_string_to_block_length(string,length):      #get back padded bytes
    arr = bytearray(utf8_string_to_bytes(string))
    if len(arr) < length:
        to_pad_byte = length - len(arr)
        for i in range(0,length-len(arr)):
            arr.append(to_pad_byte)
    return bytes(arr)

def random_AES_key():       #returns random AES key in hex
    return randbytes(16).hex()

def pad_to_AES_block_size(message):     #message in hex
    byte_size = len(message)/2
    if byte_size % 16 != 0:
        to_pad_bytes = (int)(16 * (byte_size//16 + 1) - byte_size)
        to_pad_hex = hex(to_pad_bytes)[2:]
        if len(to_pad_hex) != 2:
            to_pad_hex = '0' + to_pad_hex
        to_pad_hex = to_pad_hex * to_pad_bytes
        message = message + to_pad_hex
    return message

def decrypt_AES_ECB(key, encrypted):   #encrypted in hex, key in hex, returns hex
    key = bytes.fromhex(key)
    blocks = list(map(''.join, zip(*[iter(encrypted)]*16*2)))   #16 bytes = 128 bits = 1 AES block 
    message = bytearray()
    decipher = AES.new(key, AES.MODE_ECB)
    for block in blocks:
        message+=decipher.decrypt(hex_to_bytes(block))
    return message.hex()

def get_AES_blocks_from_hex(message):       # assumes hex message is multiple of AES block size
    blocks = list(map(''.join, zip(*[iter(message)]*16*2)))
    return blocks

def encrypt_AES_ECB(key, message):      #message in hex, key in hex, returns hex
    key = bytes.fromhex(key)
    message = pad_to_AES_block_size(message)
    blocks = list(map(''.join, zip(*[iter(message)]*16*2)))
    cipher = bytearray()
    decipher = AES.new(key, AES.MODE_ECB)
    for block in blocks:
        cipher+=decipher.encrypt(hex_to_bytes(block))
    return cipher.hex()

def decrypt_AES_CBC(key, encrypted, IV="00"*16):    #encrypted in hex, key in hex, returns hex
    key = bytes.fromhex(key)
    blocks = list(map(''.join, zip(*[iter(encrypted)]*16*2)))   #16 bytes = 128 bits = 1 AES block
    message = ""
    decipher = AES.new(key, AES.MODE_ECB)
    prev_ciphertext = IV
    for block in blocks:
        intermediate_block = decipher.decrypt(hex_to_bytes(block)).hex()
        message_block = xor_2_hex_strings(intermediate_block,prev_ciphertext)
        message += message_block
        prev_ciphertext = block
    return message

def encrypt_AES_CBC(key, message, IV="00"*16):      #encrypted in hex, key in hex, returns "IV + cipher"
    key = bytes.fromhex(key)
    message = pad_to_AES_block_size(message)
    blocks = list(map(''.join, zip(*[iter(message)]*16*2)))
    cipher = IV
    decipher = AES.new(key, AES.MODE_ECB)
    prev_encryption = IV
    for block in blocks:
        to_encrypt = xor_2_hex_strings(prev_encryption,block)
        to_add = decipher.encrypt(hex_to_bytes(to_encrypt)).hex()
        cipher += to_add
        prev_encryption=to_add
    return cipher

def detect_ECB_or_CBC(encryption_function):      # returns 1 if ECB, 2 if CBC, cipher in hex, have to pass the encryption_function, function takes in plaintext only (not hex)
    plaintext = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    cipher = encryption_function(plaintext)
    blocks = get_AES_blocks_from_hex(cipher)
    for i in range(0,len(blocks)):
        for j in range(i+1,len(blocks)):
            if blocks[i] == blocks[j]:
                return 1
    return 2

def english_plaintext_score(s):   #scores a string based on english letter frequency (chi squared test)
    expected_frequencies = {
        'e':12.02,
        't':9.10,
        'a':8.12,
        'o':7.68,
        'i':7.31,
        'n':6.95,
        's':6.28,
        'r':6.02,
        'h':5.92,
        'd':4.32,
        'l':3.98,
        'u':2.88,
        'c':2.71,
        'm':2.61,
        'f':2.30,
        'y':2.11,
        'w':2.09,
        'g':2.03,
        'p':1.82,
        'b':1.49,
        'v':1.11,
        'k':0.69,
        'x':0.17,
        'q':0.11,
        'j':0.10,
        'z':0.07
    }
    s = s.lower()
    letter_counts = {}
    total = 0
    for i in range(0,26):
        letter = chr(97+i)
        x = s.count(letter)
        # print(x)
        # print(letter)
        letter_counts[letter] = x
        total+=x
    chi = 0
    for i in range(0,26):
        letter = chr(97+i)
        observed_frequency = letter_counts[letter]/total * 100
        expected_frequency = expected_frequencies[letter]
        chi += ((observed_frequency-expected_frequency)**2)/expected_frequency
    return chi

def get_best_english_plaintext(arr):    #takes array of strings and returns most sensible english plaintext (based on chi squared test)
    min = float('inf')
    res = ""
    for s in arr:
        try:
            score = english_plaintext_score(s)
            if score < min:
                min = score
                res = s
        except Exception as e:
            pass
    return res