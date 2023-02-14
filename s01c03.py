from helper import *

def get_text(s):
    arr = []
    for i in range(65,91):
        char_hex_string = hex(i)[2:] * (int)(len(s)/2)
        xored_string = xor_2_hex_strings(s,char_hex_string)
        # print(len(xored_string))
        # print(len(char_hex_string))
        # print(xored_string)
        # print(char_hex_string)
        # print("-----------")
        # print(xored_string)
        try:
            res = hex_to_ascii_string(xored_string)
            arr.append(res)
        except:
            pass
    return arr

arr = get_text("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
result = get_best_english_plaintext(arr)
print(result)