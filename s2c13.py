from helper import *
import random

def key_value_parsing_routine(string):
    dict = {}
    key_value_pairs = string.split('&')
    for pair in key_value_pairs:
        arr = pair.split('=')
        dict[arr[0]] = arr[1]
    return dict

def profile_for(email_id):
    email_id = email_id.replace('&','')
    email_id = email_id.replace('=','')
    uid = random.randint(10,99)
    profile_string = "email="+email_id+"&uid="+str(uid)+"&role=user"
    return profile_string

key = random_AES_key()

def encrypt_user_profile(profile_string):
    profile_string = string_to_hex(profile_string)
    return encrypt_AES_ECB(key, profile_string)

def decrypt_user_profile(cipher):       # cipher in hex
    hex_decrypted = decrypt_AES_ECB(key, cipher)
    hex_decrypted = remove_valid_PKCS7_padding(hex_decrypted)
    return key_value_parsing_routine(hex_to_ascii_string(hex_decrypted))

user_input = "foooo@bar.com"   #13 bytes
cipher = encrypt_user_profile(profile_for(user_input))

# here we will customize the user_input such that 'user' happens to be at the last block of the plaintext
# this attack basically demonstrates the following: the attacker makes a profile for an email address he has
# he gets back the cipher from the server that has a role = user embedded in it.
# now he has to generate a valid ciphertext that will have role = admin using the same email id
# email=_____&uid=__&role= -> this takes 19 bytes without the email, so email has to be of 13 bytes, to have 'user' at the last block

blocks = get_AES_blocks_from_hex(cipher)[:-1]   # has blocks of 'email=foooo@bar.com&uid=XX&role='

# we need encryption of 'admin'

padded_admin_string = bytes_to_utf8_string(pad_string_to_block_length('admin',16))
email = "ten@bytes." + padded_admin_string
admin_cipher = encrypt_user_profile(profile_for(email))
admin_block = get_AES_blocks_from_hex(admin_cipher)[1]

blocks.append(admin_block)
final_cipher = ''.join(blocks)
print("Cipher:"+final_cipher)
print('--------------')
profile = decrypt_user_profile(final_cipher)
print("Profile:\n",profile)