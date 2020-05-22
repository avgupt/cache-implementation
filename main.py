import directive, associative, set_associative

def take_input(var):
    return int(input(var + ": "))

main_memory = take_input("Main memory size")
block_size = take_input("Block size")
cache_size = take_input("Cache size")
set_size = take_input("n for n way mapping")

while(True):
    mapping = input("Directive(D)/Associative(A)/Set-associative(S): ")
    if mapping == "D": directive.directive(main_memory, block_size, cache_size)
    elif mapping == "A": associative.associative(main_memory, block_size, cache_size)
    elif mapping == "S": set_associative.set_associative(main_memory, block_size, cache_size, set_size)
