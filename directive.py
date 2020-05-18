import sys, math

def take_input(var):
    return int(input(var + ": "))

main_memory = take_input("Main memory size")
block_size = take_input("Block size")
block_num = main_memory // block_size

cache_size = take_input("Cache size")
line_size = block_size
if cache_size < line_size: sys.exit("ERROR: Invalid cache size")
line_num = cache_size // line_size

block_offset = int(math.log(block_size, 2))
memory_bits = int(math.log(main_memory, 2))
if block_offset > memory_bits: sys.exit("ERROR: Block size cannot be greater than memory size.")
block_num_bits = memory_bits - block_offset

line_bits = int(math.log(line_num, 2))
tag_bits = memory_bits - line_bits - block_offset
if tag_bits < 0: sys.exit("ERROR: Invalid input.")

def decimalToBinary(n):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2)
    ans += str(n%2)
    return ans

def initialize_cache():
    global line_num, line_bits, block_offset, block_size
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

def input_new_block(cache_memory):
    global memory_bits, tag_bits, line_bits
    memory = input("> Memory address: ")
    if len(memory) != memory_bits: sys.exit("ERROR: Invalid memory address")
    data = input("> Data: ")
    tag = memory[:tag_bits]
    line = memory[tag_bits:tag_bits+line_bits]
    offset = memory[tag_bits+line_bits:]
    return cache_loading(cache_memory, data, tag, line, offset)

def cache_loading(cache_memory, data, tag, line, offset):
    if len(cache_memory[line][0]) == 0:
        cache_memory[line][0] = tag
        cache_memory[line][1][offset] = data
    elif cache_memory[line][0] == tag:
        if cache_memory[line][1][offset] != '': print("Replaced data (" + cache_memory[line][1][offset] + ")")
        cache_memory[line][1][offset] = data
    else: return replace_block(cache_memory, data, tag, line, offset)
    return cache_memory

def replace_block(cache_memory, data, tag, line, offset):
    print("Replaced tag " + cache_memory[line][0] + " with " + tag)
    cache_memory[line][0] = tag
    global block_size
    for key in cache_memory[line][1].keys():
        if len(cache_memory[line][1][key]) != 0:
            print("Deleted " + cache_memory[line][1][key])
            cache_memory[line][1][key] = ''
            if key == offset:
                cache_memory[line][1][key] = data
    return cache_memory

def cache_searching(cache_memory, address):
    global line_bits, tag_bits, memory_bits
    tag = address[:tag_bits]
    line = address[tag_bits:tag_bits+line_bits]
    offset = address[tag_bits+line_bits:]
    if len(address) != memory_bits: sys.exit("ERROR: Invalid memory address")
    if cache_memory[line][0] != tag: return "MISS"
    print("HIT ", end = "")
    return " Data: " + cache_memory[line][1][offset]

def print_cache(cache_memory):
    for line in cache_memory.keys():
        if len(cache_memory[line][0]) != 0:
            for offset in cache_memory[line][1].keys():
                print(cache_memory[line][0] + line + offset, cache_memory[line][1][offset])

print("Initialising cache ...")
cache_memory = initialize_cache()
print("Initialisation successful!")

print("############### Directive Mapping ###############")
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