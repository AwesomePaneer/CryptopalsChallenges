from helper import *
import random

key = random_AES_key()

def encryption_oracle(input):       # input in hex
    to_append = base64_to_hex("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    to_encrypt = random.randbytes(random.randrange(5,10)).hex()+input+to_append
    return encrypt_AES_ECB(key, to_encrypt)

# my challenge 12 detect_block_size wouldn't work here although it is not very hard to detect the size anyways
# so detection & prediction of encryption mechanism is skipped here (we know it is ECB)

block_size = 16
unknown_string = ""
hex_block_size = 2 * block_size

