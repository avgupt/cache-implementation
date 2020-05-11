import math, sys

def take_input(var):
    print(var, end = ": ")
    if(input("Is your input in bytes? [Y/N] ") == "Y"): return int(input(var + ": "))
    return int(input()) * pow(2,10)    # input in KB

memory_size = take_input("Memory size")
cache_lines_num = take_input("Number of cache lines")
block_size =   take_input("Block size")
 
cache_line_bits = int(math.log(cache_lines_num, 2))
block_bits = int(math.log(block_size, 2))
tag_bits = block_bits - cache_line_bits
word_bits = int(math.log(memory_size, 2)) - block_bits

def decimalToBinary(n, bitLength):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2, bitLength)
    ans += str(n%2)
    return ans if len(ans) == bitLength else "0" * (bitLength - len(ans)) + ans

def initialize_cache(tag, line, word):
    cache_memory = {}
    for i in range(line):
        cache_memory[decimalToBinary(i, line)] = ["|_" * tag, "|_" * word]
    
    return cache_memory

def input_new_block(block, tag, word, cache_memory):
    print(block + word)
    memory = input("> Memory address: ")
    
    if len(memory) != block + word: sys.exit("ERROR: Invalid memory address")
    data = input("> Word: ")
    return cache_loading([memory[:tag], memory[tag:block], data], cache_memory)

def cache_loading(n, cache_memory):
    cache_memory[n[1]] = [n[0], n[2]]
    return cache_memory

def cache_searching(cache_memory, address):
    if cache_memory[address[tag_bits:block_bits + 1]][0] != address[:tag_bits]: return "MISS"
    print("HIT ", end = "")
    return " WORD: " + cache_memory[address[tag_bits:block_bits]][1]

def print_cache(cache_memory):
    for cache_line in cache_memory.keys():
        print(cache_memory[cache_line][0] + " " + cache_line + " " + cache_memory[cache_line][1])

print("Initialising cache ...")
cache_memory = initialize_cache(tag_bits, cache_line_bits, word_bits)
print("Initialisation successful!")

print("############### Directive Mapping ###############")
print("\n\nTo print cache memory, type 'P'.\n To exit, type 'E'.\n\n\n")
while(True):
    input_task = input("Load(L)/Search(S): ")
    if input_task == "L": cache_memory = input_new_block(block_bits, tag_bits, word_bits, cache_memory)
    elif input_task == "S":
        address = input("> Address: ")
        print(cache_searching(cache_memory, address))
    elif input_task == "P": print_cache(cache_memory)
    elif input_task == "E": sys.exit("EXIT")
    else: print("Invalid input. Please try again.")