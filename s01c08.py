from helper import *

filename = "s1c8.txt"
hexcodes = []
with open(filename) as file:
    hexcodes = file.readlines()
    hexcodes = [line.rstrip() for line in hexcodes]

possible_hexcodes = set()
for hexcode in hexcodes:
    blocks = list(map(''.join, zip(*[iter(hexcode)]*16*2)))
    for i in range(0,len(blocks)):
        for j in range(i+1,len(blocks)):
            if blocks[i] == blocks[j]:
                possible_hexcodes.add(hexcode)

print(possible_hexcodes)