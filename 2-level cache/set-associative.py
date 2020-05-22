import sys, math, copy
from collections import OrderedDict

def take_input(var):
    return int(input(var + ": "))

main_memory = take_input("Main memory size")
block_size = take_input("Block size")
block_num = main_memory // block_size

l1_cache_size = take_input("Level 1 cache size")
line_size = block_size
if l1_cache_size < line_size: sys.exit("ERROR: Invalid cache size")
l1_line_num = l1_cache_size // line_size

l2_cache_size = l1_cache_size * 2
l2_line_num = l2_cache_size // line_size

set_size = take_input("n for n way mapping")
l1_set_num = l1_line_num // set_size
if l1_set_num < 1: sys.exit("ERROR: Invalid set size")
l1_set_bits = int(math.log(l1_set_num, 2))

l2_set_num = l2_line_num // set_size
l2_set_bits = int(math.log(l2_set_num, 2))

block_offset = int(math.log(block_size, 2))
memory_bits = int(math.log(main_memory, 2))
if block_offset > memory_bits: sys.exit("ERROR: Block size cannot be greater than memory size.")
block_num_bits = memory_bits - block_offset

l1_tag_bits = memory_bits - l1_set_bits - block_offset
if l1_tag_bits < 0: sys.exit("ERROR: Invalid input.")

l2_tag_bits = memory_bits - l2_set_bits - block_offset
if l2_tag_bits < 0: sys.exit("ERROR: Invalid input.")

def decimalToBinary(n):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2)
    ans += str(n%2)
    return ans

def initialize_cache():
    global l1_set_num, l1_set_bits, l2_set_num, l2_set_bits
    l1_cache_memory = {}
    for i in range(l1_set_num):
        set_in_bin = decimalToBinary(i)
        set_ = set_in_bin if len(set_in_bin) == l1_set_bits else "0" * (l1_set_bits - len(set_in_bin)) + set_in_bin
        l1_cache_memory[set_] = OrderedDict()
    l2_cache_memory = {}
    for j in range(l2_set_num):
        set_in_bin = decimalToBinary(j)
        set_ = set_in_bin if len(set_in_bin) == l2_set_bits else "0" * (l2_set_bits - len(set_in_bin)) + set_in_bin
        l2_cache_memory[set_] = OrderedDict()   
    return l1_cache_memory, l2_cache_memory

def create_block():
    global block_size, block_offset

    block = {}
    for i in range(block_size):
        offset_in_bin = decimalToBinary(i)
        offset_ = offset_in_bin if len(offset_in_bin) == block_offset else "0" * (block_offset - len(offset_in_bin)) + offset_in_bin
        block[offset_] = ''
    return block

def input_new_block():
    global memory_bits, l1_tag_bits, l1_set_bits, l1_cache_memory
    memory = input("> Memory address: ")
    if len(memory) != memory_bits: sys.exit("ERROR: Invalid memory address")
    data = input("> Data: ")
    tag = memory[:l1_tag_bits]
    set_ = memory[l1_tag_bits:l1_tag_bits + l1_set_bits]
    offset = memory[l1_tag_bits + l1_set_bits:]
    return l1_cache_loading(data, tag, set_, offset)

def l1_cache_loading(data, tag, set_, offset):
    global set_size, l1_cache_memory, block
    if len(l1_cache_memory[set_]) >= set_size and tag not in l1_cache_memory[set_].keys(): return l1_replace_block(data, tag, set_, offset)
    if tag in l1_cache_memory[set_].keys() and len(l1_cache_memory[set_][tag][offset]) > 0:
        print("Data " + l1_cache_memory[set_][tag][offset] + " deleted")
    elif tag not in l1_cache_memory[set_].keys():
        l1_cache_memory[set_][tag] = copy.copy(block)
    l1_cache_memory[set_][tag][offset] = data

def l1_replace_block(data, tag, set_, offset):
    """ Uses first in first out"""
    global l2_tag_bits, l2_set_bits, l2_cache_memory, block

    memory = tag + set_ + offset
    l2_tag = memory[:l2_tag_bits]
    l2_set_ = memory[l2_tag_bits:l2_tag_bits + l2_set_bits]
    if l2_tag in l2_cache_memory[l2_set_].keys():
        l2_to_l1_loading(memory, l2_cache_memory[l2_set_][l2_tag])
        l1_cache_memory[set_][tag][offset] = data
        return

    cache_entry = l1_cache_memory[set_].popitem(last=False)
    memory_block = [set_, cache_entry[0], cache_entry[1]]
    l2_cache_loading(copy.deepcopy(memory_block))
    print("Loading", tag + set_ + offset, "in level 1.\nReplaced block " + memory_block[1] + memory_block[0] + " with " + tag)
    l1_cache_memory[set_][tag] = copy.copy(block)
    l1_cache_memory[set_][tag][offset] = data

def l2_cache_loading(memory_block):
    global l2_cache_memory, l2_cache_size, block, l2_tag_bits, l2_set_bits
    memory = memory_block[1] + memory_block[0]
    tag = memory[:l2_tag_bits]
    set_ = memory[l2_tag_bits:l2_tag_bits+l2_set_bits]
    offset_dict = memory_block[2]
    print("Loading block", tag + set_, "in level 2 cache.")
    if len(l2_cache_memory[set_]) >= set_size and tag not in l2_cache_memory[set_].keys(): return l2_replace_block(tag, set_, offset_dict)
    l2_cache_memory[set_][tag] = offset_dict

def l2_replace_block(tag, set_, offset_dict):
    """ Uses first in first out"""
    global l2_cache_memory
    cache_entry = l2_cache_memory[set_].popitem(last=False)
    print("Replaced block " + cache_entry[0] + set_ + " with " + tag + set_)
    l2_cache_memory[set_][tag] = offset_dict

def l1_cache_searching(address):
    global l1_set_bits, l1_tag_bits, memory_bits, l1_cache_memory
    tag = address[:l1_tag_bits]
    set_ = address[l1_tag_bits : l1_tag_bits + l1_set_bits]
    offset = address[l1_tag_bits + l1_set_bits :]
    if len(address) != memory_bits: sys.exit("ERROR: Invalid memory address")
    if tag not in l1_cache_memory[set_].keys():
        print("MISS: Address not found in level 1 cache")
        l2_cache_searching(address)
    else: print("HIT: Address found in level 1 cache.", "Data: " + l1_cache_memory[set_][tag][offset])

def l2_cache_searching(address):
    global l2_cache_memory, l2_tag_bits, l2_set_bits
    tag = address[:l2_tag_bits]
    set_ = address[l2_tag_bits : l2_tag_bits + l2_set_bits]
    offset = address[l2_tag_bits+l2_set_bits:]
    if tag not in l2_cache_memory[set_].keys(): print("MISS: Address not found in level 2 cache")
    else:
        print("HIT: Address found in level 2 cache.", "Data: " + l2_cache_memory[set_][tag][offset])
        return l2_to_l1_loading(address, copy.copy(l2_cache_memory[set_][tag]))

def l2_to_l1_loading(address, offset_dict):
    print("Loading block corresponding to", address, "in level 1 cache.")
    global l2_cache_memory, l2_tag_bits, l2_set_bits, l1_set_bits, l1_tag_bits, l1_cache_memory
    tag = address[:l2_tag_bits]
    set_ = address[l2_tag_bits : l2_tag_bits + l2_set_bits]
    offset = address[l2_tag_bits+l2_set_bits:]
    l1_tag = address[:l1_tag_bits]
    l1_set_ = address[l1_tag_bits : l1_tag_bits + l1_set_bits]
    cache_entry = l1_cache_memory[l1_set_].popitem(last=False)
    print("Replaced block " + cache_entry[0] + l1_set_ + " with " + tag + set_, "in level 1 cache")
    memory_block = [l1_set_, cache_entry[0], cache_entry[1]]
    l2_cache_loading(memory_block)
    l1_cache_memory[l1_set_][l1_tag] = offset_dict

def print_cache(cache_memory):
    for set_ in cache_memory.keys():
        for tag in cache_memory[set_].keys():
            for offset in cache_memory[set_][tag].keys():
                print(tag + set_ + offset, cache_memory[set_][tag][offset])
        print('----')

print("Initialising cache ...")
l1_cache_memory, l2_cache_memory = initialize_cache()
print(l1_cache_memory)
print(l2_cache_memory)
block = create_block()
print("Initialisation successful!")

print("############### Set-associative Mapping ###############")
print("\nTo print cache memory, type 'P'.\n To exit, type 'E'.\n")
while(True):
    input_task = input("Read(R)/Write(W): ")
    if input_task == "W": input_new_block()
    elif input_task == "R":
        address = input("> Address: ")
        l1_cache_searching(address)
    elif input_task == "P":
        print("LEVEL 1")
        print_cache(l1_cache_memory)
        print('#' * 20)
        print("LEVEL 2")
        print_cache(l2_cache_memory)
    elif input_task == "E": sys.exit("EXIT")
    else: print("Invalid input. Please try again.")