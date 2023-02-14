from numpy import block
from helper import *

key = random_AES_key()

def first_function(input_string):       # input_string in plaintext
    input_string = input_string.replace(';','')
    input_string = input_string.replace('=','')
    input_string = r"comment1=cooking%20MCs;userdata=" + input_string + r";comment2=%20like%20a%20pound%20of%20bacon"
    cipher = encrypt_AES_CBC(key,string_to_hex(input_string))
    return cipher

def second_function(cipher):            # cipher in hex
    decrypted = decrypt_AES_CBC(key,cipher)
    return (string_to_hex('admin=true') in decrypted)

input_string = "i know this str."
cipher = first_function(input_string)
blocks = get_AES_blocks_from_hex(cipher)

# we know 1st prepending string is of 32 bytes, so our string will be at 3rd plaintext block
# so we know the 3rd plaintext block basically
# m[3] = D(c[3]) xor c[2]       ---> in CBC (3rd plaintext block is m[3] and m[0] is IV)
# if we do c[2] = c[2] xor (19 bytes of m[3]) xor (hex of 'admin=true'), m[3] should decrypt to having admin=true

to_xor_2 = string_to_hex(";admin=true")
to_xor_1 = string_to_hex(input_string[:len(to_xor_2)])
temp_1 = xor_2_hex_strings(to_xor_1,to_xor_2)
temp_2 = xor_2_hex_strings(blocks[2],temp_1)
temp_3 = temp_2 + blocks[2][len(to_xor_2):]        # as 'i know thi' is start of m[3] and rest we just keep as is
blocks[2] = temp_3
cipher = ''.join(blocks)
print(second_function(cipher))