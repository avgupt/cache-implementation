import sys, math
from collections import OrderedDict

def take_input(var):
    return int(input(var + ": "))

main_memory = take_input("Main memory size")
block_size = take_input("Block size")
block_num = main_memory // block_size

cache_size = take_input("Cache size")
line_size = block_size
if cache_size < line_size: sys.exit("ERROR: Invalid cache size")
line_num = cache_size // line_size

set_size = take_input("n for n way mapping")
set_num = line_num // set_size
if set_num < 1: sys.exit("ERROR: Invalid set size")
set_bits = int(math.log(set_num, 2))

block_offset = int(math.log(block_size, 2))
memory_bits = int(math.log(main_memory, 2))
if block_offset > memory_bits: sys.exit("ERROR: Block size cannot be greater than memory size.")
block_num_bits = memory_bits - block_offset

tag_bits = memory_bits - set_bits - block_offset
if tag_bits < 0: sys.exit("ERROR: Invalid input.")

def decimalToBinary(n):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2)
    ans += str(n%2)
    return ans

def initialize_cache():
    global set_num, set_bits
    cache_memory = {}
    for i in range(set_num):
        set_in_bin = decimalToBinary(i)
        set_ = set_in_bin if len(set_in_bin) == set_bits else "0" * (set_bits - len(set_in_bin)) + set_in_bin
        cache_memory[set_] = OrderedDict()
    return cache_memory

def input_new_block(cache_memory):
    global memory_bits, tag_bits, set_bits
    memory = input("> Memory address: ")
    if len(memory) != memory_bits: sys.exit("ERROR: Invalid memory address")
    data = input("> Data: ")
    tag = memory[:tag_bits]
    set_ = memory[tag_bits:tag_bits + set_bits]
    offset = memory[tag_bits + set_bits:]
    return cache_loading(cache_memory, data, tag, set_, offset)

def cache_loading(cache_memory, data, tag, set_, offset):
    global set_size, block_offset, block_size
    if len(cache_memory[set_]) >= set_size and tag not in cache_memory[set_].keys():return replace_block(cache_memory, data, tag, set_, offset)
    if tag in cache_memory[set_].keys() and len(cache_memory[set_][tag][offset]) > 0:
        print("Data " + cache_memory[set_][tag][offset] + " deleted")
    elif tag not in cache_memory[set_].keys():
        cache_memory[set_][tag] = {}
        for i in range (block_size):
            offset_in_bin = decimalToBinary(i)
            offset_ = offset_in_bin if len(offset_in_bin) == len(offset) else "0" * (len(offset) - len(offset_in_bin)) + offset_in_bin
            cache_memory[set_][tag][offset_] = ''
    cache_memory[set_][tag][offset] = data
    return cache_memory

def replace_block(cache_memory, data, tag, set_, offset):
    """ Uses first in first out"""
    global block_offset, block_size
    cache_entry = cache_memory[set_].popitem(last=False)
    print("Removed tag: " + cache_entry[0])
    cache_memory[set_][tag] = {}
    for i in range(block_size):
        offset_in_bin = decimalToBinary(i)
        offset_ = offset_in_bin if len(offset_in_bin) == len(offset) else "0" * (len(offset) - len(offset_in_bin)) + offset_in_bin
        cache_memory[set_][tag][offset_] = ''
    cache_memory[set_][tag][offset] = data
    return cache_memory

def cache_searching(cache_memory, address):
    global set_bits, tag_bits, memory_bits
    tag = address[:tag_bits]
    set_ = address[tag_bits : tag_bits + set_bits]
    offset = address[tag_bits + set_bits :]
    if len(address) != memory_bits: sys.exit("ERROR: Invalid memory address")
    if tag not in cache_memory[set_].keys(): return "MISS"
    print("HIT ", end = "")
    return " Data: " + cache_memory[set_][tag][offset]

def print_cache(cache_memory):
    for set_ in cache_memory.keys():
        for tag in cache_memory[set_].keys():
            for offset in cache_memory[set_][tag].keys():
                print(tag + set_ + offset, cache_memory[set_][tag][offset])
        print()

print("Initialising cache ...")
cache_memory = initialize_cache()
print("Initialisation successful!")

print("############### Set-associative Mapping ###############")
print("\nTo print cache memory, type 'P'.\n To exit, type 'E'.\n")
while(True):
    input_task = input("Read(R)/Write(W): ")
    if input_task == "W": cache_memory = input_new_block(cache_memory)
    elif input_task == "R":
        address = input("> Address: ")
        print(cache_searching(cache_memory, address))
    elif input_task == "P": print_cache(cache_memory)
    elif input_task == "E": sys.exit("EXIT")
    else: print("Invalid input. Please try again.")