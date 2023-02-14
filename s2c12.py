from helper import *

key = random_AES_key()

def encryption_oracle(input):       # input in hex
    to_append = base64_to_hex("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    to_encrypt = input + to_append
    return encrypt_AES_ECB(key, to_encrypt)

plaintext = "the text here does not matter"
cipher = encryption_oracle(string_to_hex(plaintext))
def detect_block_size():
    size = 1     # bytes
    initial_length = len(encryption_oracle(string_to_hex(plaintext[:size])))
    while True:
        size+=1
        c = encryption_oracle(string_to_hex(plaintext[:size]))
        if not len(c)==initial_length:
            return int(len(c) - initial_length)/2      # /2 since cipher in hex but size in bytes

block_size = (int)(detect_block_size())     # bytes
print("Block size (bytes):"+str(block_size))
print("Encryption Mechanism (1 if ECB):",detect_ECB_or_CBC(encryption_oracle))     # 1 -> ECB
# attack starts now
unknown_string = ""
number_of_blocks = 9    #try diff sizes (we know it in this case) - keep increasing until you reach gibberish (000000...) OR you are sure the entire prefix is retrieved
hex_block_size = 2 * block_size
for k in range(0,number_of_blocks):
    for j in range(0,block_size):
        input_block = string_to_hex("A"*(block_size-j-1))
        input_cipher = encryption_oracle(input_block)
        for i in range(0,256):
            hex_int = get_hex_from_int(i)
            test_input = input_block+unknown_string+hex_int
            test_cipher = encryption_oracle(test_input)
            if test_cipher[k*hex_block_size:(k+1)*hex_block_size] == input_cipher[k*hex_block_size:(k+1)*hex_block_size]:
                unknown_string+=hex_int
                break
print("Hex:\n"+unknown_string)
print("----\nAscii:\n"+hex_to_ascii_string(unknown_string))