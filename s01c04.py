from helper import *

def get_xored_array(s,start_ascii,end_ascii):
    arr = []
    for i in range(start_ascii,end_ascii):
        char_hex_string = hex(i)[2:] * (int)(len(s)/2)
        xored_string = xor_2_hex_strings(s,char_hex_string)
        arr.append(xored_string)
    return arr

filename = "s1c4.txt"
lines = []
with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

index = 0
possible_hex = {}
length = lines[0]
for line in lines:
    arr = get_xored_array(line,32,128)
    possible_decodes = []
    for item in arr:
        decoded = ""
        try:
            decoded = hex_to_ascii_string(item)
            if is_ascii_english(decoded):
                possible_decodes.append(decoded)
        except Exception as e:
            # print(e)
            pass
    if len(possible_decodes) > 0:
        possible_hex[line] = possible_decodes

possible_result = []
for key in possible_hex:
    possible_result += possible_hex[key]

result = get_best_english_plaintext(possible_result)
for key in possible_hex:
    if result in possible_hex[key]:
        print(key)
        print(result)
