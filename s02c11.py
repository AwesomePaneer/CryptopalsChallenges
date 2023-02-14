from helper import *
import random

def encryption_oracle(input):
    key = random_AES_key()
    bytes_to_encrypt = utf8_string_to_bytes(input)
    bytes_to_encrypt = random.randbytes(random.randrange(5,10)) + bytes_to_encrypt + random.randbytes(random.randrange(5,10))
    hex_to_encrypt = bytes_to_encrypt.hex()
    choice = random.randint(1,2)
    print("Choice:"+str(choice))
    if choice == 1:
        return encrypt_AES_ECB(key, hex_to_encrypt)
    else:
        IV = random.randbytes(16).hex()
        return encrypt_AES_CBC(key, hex_to_encrypt, IV)

for i in range(1,10):
    print(detect_ECB_or_CBC(encryption_oracle))
    print("-------------------------")