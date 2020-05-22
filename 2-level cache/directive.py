import sys, math, copy

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

l1_line_bits = int(math.log(l1_line_num, 2))
l1_tag_bits = memory_bits - l1_line_bits - block_offset
if l1_tag_bits < 0: sys.exit("ERROR: Invalid input.")

l2_line_bits = int(math.log(l2_line_num, 2))
l2_tag_bits = memory_bits - l2_line_bits - block_offset
if l2_tag_bits < 0: sys.exit("ERROR: Invalid input.")

def decimalToBinary(n):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2)
    ans += str(n%2)
    return ans

def initialize_cache(line_num, line_bits):
    global block_offset, block_size
    block = {}
    cache_memory = {}
    for i in range(line_num):
        line_in_bin = decimalToBinary(i)
        line = line_in_bin if len(line_in_bin) == line_bits else "0" * (line_bits - len(line_in_bin)) + line_in_bin
        cache_memory[line] = ['', {}]
        for j in range(block_size):
            offset_in_bin = decimalToBinary(j)
            offset = offset_in_bin if len(offset_in_bin) == block_offset else "0" * (block_offset - len(offset_in_bin)) + offset_in_bin
            cache_memory[line][1][offset] = ''
    return cache_memory

def input_new_block():
    global memory_bits, l1_tag_bits, l1_line_bits
    memory = input("> Memory address: ")
    if len(memory) != memory_bits: sys.exit("ERROR: Invalid memory address")
    data = input("> Data: ")
    tag = memory[:l1_tag_bits]
    line = memory[l1_tag_bits:l1_tag_bits+l1_line_bits]
    offset = memory[l1_tag_bits+l1_line_bits:]
    return l1_cache_loading(data, tag, line, offset)

def l1_cache_loading(data, tag, line, offset):
    global l1_cache_memory, l2_cache_loading
    if len(l1_cache_memory[line][0]) == 0:
        l1_cache_memory[line][0] = tag
        l1_cache_memory[line][1][offset] = data
    elif l1_cache_memory[line][0] == tag:
        if l1_cache_memory[line][1][offset] != '': print("Data " + l1_cache_memory[line][1][offset] + " deleted")
        l1_cache_memory[line][1][offset] = data
    else: return l1_replace_block(data, tag, line, offset)

def l1_replace_block(data, tag, line, offset):
    global l1_cache_memory, l2_line_bits, l2_tag_bits, l2_cache_memory

    memory = tag + line + offset
    l2_line = memory[l2_tag_bits:l2_tag_bits+l2_line_bits]
    l2_tag = memory[:l2_tag_bits]
    if l2_cache_memory[l2_line][0] == l2_tag:
        l2_to_l1_loading(memory, l2_cache_memory[l2_line][1])
        l1_cache_memory[line][1][offset] = data
        return

    memory_block = [l1_cache_memory[line][0] + line + offset, l1_cache_memory[line][1]]
    l2_cache_loading(copy.deepcopy(memory_block))
    print("Loading", tag + line + offset, "in level 1.\nReplaced tag " + l1_cache_memory[line][0] + " with " + tag)
    l1_cache_memory[line][0] = tag
    global block_size
    for key in l1_cache_memory[line][1].keys():
        if len(l1_cache_memory[line][1][key]) != 0:
            l1_cache_memory[line][1][key] = ''        
    l1_cache_memory[line][1][offset] = data

def l2_cache_loading(memory_block):
    global l2_tag_bits, l2_line_bits, l2_cache_memory, l2_cache_size
    memory = memory_block[0]
    tag = memory[:l2_tag_bits]
    line = memory[l2_tag_bits:l2_tag_bits+l2_line_bits]
    print("Loading block", memory[:l2_tag_bits+l2_line_bits], "in level 2 cache.")
    if l2_cache_memory[line][0] == tag:
        l2_cache_memory[line][1] = memory_block[1]
    elif len(l2_cache_memory[line][0]) == 0:
        l2_cache_memory[line][0] = tag
        l2_cache_memory[line][1] = memory_block[1]
    else: return l2_replace_block(tag, line, memory_block[1])

def l2_replace_block(tag, line, offset_dict):
    global l2_cache_memory
    print("Replaced tag " + l2_cache_memory[line][0] + " with " + tag)
    l2_cache_memory[line][0] = tag
    l2_cache_memory[line][1] = offset_dict

def l1_cache_searching(address):
    global memory_bits, l1_cache_memory, l1_tag_bits, l1_line_bits
    tag = address[:l1_tag_bits]
    line = address[l1_tag_bits:l1_tag_bits+l1_line_bits]
    offset = address[l1_tag_bits+l1_line_bits:]
    if len(address) != memory_bits: sys.exit("ERROR: Invalid memory address")
    if l1_cache_memory[line][0] != tag:
        print("MISS: Address not found in level 1 cache")
        l2_cache_searching(address)
    else: print("HIT: Address found in level 1 cache.", "Data: " + l1_cache_memory[line][1][offset])

def l2_cache_searching(address):
    global l2_cache_memory, l2_tag_bits, l2_line_bits
    tag = address[:l2_tag_bits]
    line = address[l2_tag_bits:l2_tag_bits+l2_line_bits]
    offset = address[l2_tag_bits+l2_line_bits:]
    if l2_cache_memory[line][0] != tag: print("MISS: Address not found in level 2 cache")
    else:
        print("HIT: Address found in level 2 cache.", "Data: " + l2_cache_memory[line][1][offset])
        return l2_to_l1_loading(address, copy.copy(l2_cache_memory[line][1]))

def l2_to_l1_loading(address, offset_dict):
    print("Loading block corresponding to", address, "in level 1 cache.")
    global l1_tag_bits, l1_line_bits, l1_cache_memory
    tag = address[:l1_tag_bits]
    line = address[l1_tag_bits:l1_tag_bits+l1_line_bits]
    offset = address[l1_tag_bits+l1_line_bits:]
    print("Replaced tag " + l1_cache_memory[line][0] + " with " + tag, "in level 1 cache")
    l2_cache_loading([l1_cache_memory[line][0] + line, copy.deepcopy(l1_cache_memory[line][1])])
    l1_cache_memory[line][0] = tag
    l1_cache_memory[line][1] = offset_dict

def print_cache(cache_memory):
    for line in cache_memory.keys():
        if len(cache_memory[line][0]) != 0:
            for offset in cache_memory[line][1].keys():
                print(cache_memory[line][0] + line + offset, cache_memory[line][1][offset])

print("Initialising cache ...")
l1_cache_memory = initialize_cache(l1_line_num, l1_line_bits)
l2_cache_memory = initialize_cache(l2_line_num, l2_line_bits)
print("Initialisation successful!")

print("############### Directive Mapping ###############")
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