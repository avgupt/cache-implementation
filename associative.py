# part of word search

import math, sys
from collections import OrderedDict
word_bits = 32
main_memory = int(input("> Memory size: "))
cache_size = int(input("> Cache size: "))

size = cache_size

memory_bits = int(math.log(main_memory,2))
cache_bits = int(int(math.log(cache_size,2)))

def decimalToBinary(n):
    ans = ""
    if(n>1):
        ans += decimalToBinary(n//2)
    ans += str(n%2)
    return ans

def initialize_cache(cache_bits, word):
    cache = OrderedDict()
    return cache

def input_new_block(cache_bits, word, cache_memory):
    data = input("> Word: ")
    if len(data) > word: sys.exit("ERROR: Invalid input.")
    if data in cache_memory.keys():
        print("Word already exists in memory. Try search.")
        return cache_memory
    return cache_loading(data, cache_bits, cache_memory)

def cache_loading(data, cache_bits, cache_memory):
    global size
    if (len(cache_memory) < size):
        memory_in_bin = decimalToBinary(len(cache_memory))
        memory = memory_in_bin if len(memory_in_bin) == cache_bits else "0" * (cache_bits - len(memory_in_bin)) + memory_in_bin
        cache_memory[data] = memory
        return cache_memory
    return replace_word(cache_memory, data)

def replace_word(cache_memory, data):
    """ Uses first in first out"""
    cache_entry = cache_memory.popitem(last=False)
    print("Replaced " + cache_entry[0] + " at address " + cache_entry[1])
    cache_memory[data] = cache_entry[1]
    return cache_memory

def cache_searching(cache_memory, word):
    if word not in cache_memory.keys(): return "MISS"
    print("HIT ", end = "")
    return " ADDRESS: " + cache_memory[word]

def print_cache(cache_memory):
    for word in cache_memory.keys():
        print(word + " " + cache_memory[word])

print("Initialising cache ...")
cache_memory = initialize_cache(cache_bits, word_bits)
print("Initialisation successful!")

print("############### Directive Mapping ###############")
print("\nTo print cache memory, type 'P'.\n To exit, type 'E'.\n")
while(True):
    input_task = input("Load(L)/Search(S): ")
    if input_task == "L": cache_memory = input_new_block(cache_bits, word_bits, cache_memory)
    elif input_task == "S":
        word = input("> Word: ")
        print(cache_searching(cache_memory, word))
    elif input_task == "P": print_cache(cache_memory)
    elif input_task == "E": sys.exit("EXIT")
    else: print("Invalid input. Please try again.")
