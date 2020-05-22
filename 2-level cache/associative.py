import sys, math, copy
from collections import OrderedDict

def take_input(var):
    return int(input(var + ": "))

main_memory = take_input("Main memory size")
block_size = take_input("Block size")
block_num = main_memory // block_size

l1_cache_size = take_input("Level 1 cache size")
l1_line_size = block_size
if l1_cache_size < l1_line_size: sys.exit("ERROR: Invalid cache size")
l1_line_num = l1_cache_size // l1_line_size

l2_cache_size = l1_cache_size * 2
l2_line_size = block_size
l2_line_num = l2_cache_size // l2_line_size

if (l1_cache_size >= l2_cache_size): sys.exit("ERROR: Level 1 cache size cannot be greater than or equal to level 2 cache size.")

block_offset = int(math.log(block_size, 2))
memory_bits = int(math.log(main_memory, 2))
if block_offset > memory_bits: sys.exit("ERROR: Block size cannot be greater than memory size.")
block_num_bits = memory_bits - block_offset

tag_bits = block_num_bits

l1_size = l1_line_num
l2_size = l2_line_num

def decimalToBinary(n):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2)
    ans += str(n%2)
    return ans

def initialize_cache():
    cache = OrderedDict()
    return cache

def create_block():
    global block_size, block_offset

    block = {}
    for i in range(block_size):
        offset_in_bin = decimalToBinary(i)
        offset_ = offset_in_bin if len(offset_in_bin) == block_offset else "0" * (block_offset - len(offset_in_bin)) + offset_in_bin
        block[offset_] = ''
    return block

def input_new_block():
    global l1_cache_memory
    global memory_bits, tag_bits
    memory = input("> Memory address: ")
    if len(memory) != memory_bits: sys.exit("ERROR: Invalid memory address")
    data = input("> Data: ")
    tag = memory[:tag_bits]
    offset = memory[tag_bits:]
    return l1_cache_loading(data, tag, offset)

def l1_cache_loading(data, tag, offset):
    global l1_cache_memory, l1_size, block_offset, block_size, block
    if len(l1_cache_memory) >= l1_size and tag not in l1_cache_memory.keys(): return l1_replace_block(data, tag, offset)
    if tag in l1_cache_memory.keys() and len(l1_cache_memory[tag][offset]) > 0:
        print("Data " + l1_cache_memory[tag][offset] +" deleted")
    elif tag not in l1_cache_memory.keys():
        l1_cache_memory[tag] = copy.deepcopy(block)
    l1_cache_memory[tag][offset] = data

def l1_replace_block(data, tag, offset):
    """ Uses first in first out"""
    global block_offset, block_size, l1_cache_memory, l2_cache_memory, block

    if tag in l2_cache_memory.keys():
        print("Address found in level 2 cache.")
        l2_to_l1_loading(tag+offset, l2_cache_memory[tag])
        l1_cache_memory[tag][offset] = data
        return

    cache_entry = l1_cache_memory.popitem(last=False)
    memory_block = [cache_entry[0], cache_entry[1]]
    l2_cache_loading(copy.deepcopy(memory_block))
    print("Loading", tag + offset, "in level 1.\nReplaced block " + cache_entry[0] + " with " + tag)
    l1_cache_memory[tag] = copy.deepcopy(block)
    l1_cache_memory[tag][offset] = data

def l2_cache_loading(memory_block):
    global l2_cache_memory, l2_cache_size, block
    print("Loading block", memory_block[0], "in level 2 cache.")
    tag = memory_block[0]
    if len(l2_cache_memory) >= l2_size and tag not in l2_cache_memory.keys(): return l2_replace_block(memory_block)
    l2_cache_memory[tag] = memory_block[1]

def l2_replace_block(memory_block):
    """ Uses first in first out"""
    global l2_cache_memory
    cache_entry = l2_cache_memory.popitem(last=False)
    print("Replaced block " + cache_entry[0] + " with " + memory_block[0])
    l2_cache_memory[memory_block[0]] = memory_block[1]

def l1_cache_searching(address):
    global tag_bits, memory_bits, l1_cache_memory
    tag = address[:tag_bits]
    offset = address[tag_bits:]
    if len(address) != memory_bits: sys.exit("ERROR: Invalid memory address")
    if tag not in l1_cache_memory.keys():
        print("MISS: Address not found in level 1 cache")
        l2_cache_searching(address)
    else: print("HIT: Address found in level 1 cache.", "Data: " + l1_cache_memory[tag][offset])

def l2_cache_searching(address):
    global tag_bits, l2_cache_memory
    tag = address[:tag_bits]
    offset = address[tag_bits:]
    if tag not in l2_cache_memory.keys(): print("MISS: Address not found in level 2 cache")
    else:
        print("HIT: Address found in level 2 cache.", "Data: " + l2_cache_memory[tag][offset])
        l2_to_l1_loading(address, copy.deepcopy(l2_cache_memory[tag]))

def l2_to_l1_loading(address, offset_dict):
    print("Loading block corresponding to", address, "in level 1 cache.")
    global l1_cache_memory, tag_bits
    tag = address[:tag_bits]
    offset = address[tag_bits:]
    cache_entry = l1_cache_memory.popitem(last=False)
    print("Replaced block " + cache_entry[0] + " with " + tag, "in level 1 cache")
    l2_cache_loading(cache_entry)
    l1_cache_memory[tag] = offset_dict

def print_cache(cache_memory):
    for tag in cache_memory.keys():
        for offset in cache_memory[tag].keys():
            print(tag + offset, cache_memory[tag][offset])

print("Initialising cache ...")
l1_cache_memory = initialize_cache()
l2_cache_memory = initialize_cache()
block = create_block()
print("Initialisation successful!")

print("############### Fully Associative Mapping ###############")
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