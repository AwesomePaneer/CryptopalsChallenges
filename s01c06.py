from helper import *

filename = 's1c6.txt'
file = open(filename,mode='r')
lines = file.read()
hex = base64_to_hex(lines)

#find hamming distance using x blocks
key_hamming_distance = {}
for keysize in range(2,41):
    number_of_blocks = 4    #experiment by changing
    blocks = list(map(''.join, zip(*[iter(hex)]*keysize*2)))[:number_of_blocks]     #keysize * 2 as one byte = 2 hex chars
    blocks_combinations = nCr_combinations(blocks,2)
    total_distance = 0
    for item in blocks_combinations:
        distance = hamming_distance(item[0],item[1])/keysize
        total_distance += distance
    total_distance /= len(blocks_combinations)
    key_hamming_distance[keysize] = total_distance

#pick x keys with min hamming distance
number_of_keys_to_proceed = 3   #experiment by changing
keysizes = []
for i in range(0,number_of_keys_to_proceed):
    minval = min(key_hamming_distance.items(), key=lambda x: x[1]) 
    keysizes.append(minval[0])
    key_hamming_distance.pop(minval[0])
# print(keysizes)

#break and transpose
possible_keys = []
for keysize in keysizes:
    blocks = list(map(''.join, zip(*[iter(hex)]*keysize*2)))
    # print(blocks)
    length = len(blocks[0])
    strings = []    #shall contain the transposed blocks - each string is one column
    for i in range(0,length,2):
        string = ""
        for block in blocks:
            string += block[i:i+2]
        strings.append(string)
    key = ""
    for string in strings:
        dict = {}
        arr = []
        for i in range(0,256):
            char_hex_string = get_hex_from_int(i) * (int)(len(string)/2)
            xored_string = xor_2_hex_strings(string,char_hex_string)
            try:
                dict[i] = hex_to_ascii_string(xored_string)
                arr.append(hex_to_ascii_string(xored_string))
            except:
                pass
        
        key_ascii_int = list(dict.keys())[list(dict.values()).index(get_best_english_plaintext(arr))]
        key += get_hex_from_int(key_ascii_int)
    if len(key)!=0:
        possible_keys.append(key)

possible_answers = []
for key in possible_keys:
    multiplier = (int)(len(hex)/len(key)) + 1
    key_string = key * multiplier
    print(hex_to_ascii_string(key))
    possible_answers.append(xor_2_hex_strings(key_string,hex))

for answer in possible_answers:
    try:
        print(hex_to_utf8_string(answer))
    except:
        pass
    print('----------------------')
