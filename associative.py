import sys, math
from collections import OrderedDict

def associative(main_memory, block_size, cache_size):

    block_num = main_memory // block_size

    line_size = block_size
    if cache_size < line_size: sys.exit("ERROR: Invalid cache size")
    line_num = cache_size // line_size

    block_offset = int(math.log(block_size, 2))
    memory_bits = int(math.log(main_memory, 2))
    if block_offset > memory_bits: sys.exit("ERROR: Block size cannot be greater than memory size.")
    block_num_bits = memory_bits - block_offset

    tag_bits = block_num_bits
    size = line_num

    def decimalToBinary(n):
        ans = ""
        if(n>1):
            ans += decimalToBinary(n//2)
        ans += str(n%2)
        return ans

    def initialize_cache():
        cache = OrderedDict()
        return cache

    def input_new_block(cache_memory):
        memory = input("> Memory address: ")
        if len(memory) != memory_bits: sys.exit("ERROR: Invalid memory address")
        data = input("> Data: ")
        tag = memory[:tag_bits]
        offset = memory[tag_bits:]
        return cache_loading(cache_memory, data, tag, offset)

    def cache_loading(cache_memory, data, tag, offset):
        if len(cache_memory) >= size and tag not in cache_memory.keys(): return replace_block(cache_memory, data, tag, offset)
        if tag in cache_memory.keys() and len(cache_memory[tag][offset]) > 0:
            print("Data " + cache_memory[tag][offset] +" deleted")
        elif tag not in cache_memory.keys():
            cache_memory[tag] = {}
            for i in range(block_size):
                offset_in_bin = decimalToBinary(i)
                offset_ = offset_in_bin if len(offset_in_bin) == block_offset else "0" * (block_offset - len(offset_in_bin)) + offset_in_bin
                cache_memory[tag][offset_] = ''
        cache_memory[tag][offset] = data
        return cache_memory

    def replace_block(cache_memory, data, tag, offset):
        """ Uses first in first out"""
        cache_entry = cache_memory.popitem(last=False)
        print("Removed tag: " + cache_entry[0])
        cache_memory[tag] = {}
        for i in range(block_size):
            offset_in_bin = decimalToBinary(i)
            offset_ = offset_in_bin if len(offset_in_bin) == block_offset else "0" * (block_offset - len(offset_in_bin)) + offset_in_bin
            cache_memory[tag][offset_] = ''
        cache_memory[tag][offset] = data
        return cache_memory

    def cache_searching(cache_memory, address):
        tag = address[:tag_bits]
        offset = address[tag_bits:]
        if len(address) != memory_bits: sys.exit("ERROR: Invalid memory address")
        if tag not in cache_memory.keys(): return "MISS"
        print("HIT ", end = "")
        return " Data: " + cache_memory[tag][offset]

    def print_cache(cache_memory):
        for tag in cache_memory.keys():
            for offset in cache_memory[tag].keys():
                print(tag + offset, cache_memory[tag][offset])

    print("Initialising cache ...")
    cache_memory = initialize_cache()
    print("Initialisation successful!")

    print("#" * 20, "Associative Mapping", "#" * 20)
    print("\nTo print cache memory, type 'P'.\n To exit, type 'E'.\n")
    while(True):
        input_task = input("Read(R)/Write(W): ")
        if input_task == "W": cache_memory = input_new_block(cache_memory)
        elif input_task == "R":
            address = input("> Address: ")
            print(cache_searching(cache_memory, address))
        elif input_task == "P": print_cache(cache_memory)
        elif input_task == "E": return
        else: print("Invalid input. Please try again.")