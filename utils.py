from collections import deque

def unsigned_to_signed(value: int) -> int:
    if value <= (2**255 - 1):
        return value
    else:
        return value - (2**256)


def signed_to_unsigned(value: int) -> int:
    if value < 0:
        return value + (2**256)
    else:
        return value
    
def print_deque(stack:deque):
    print("")
    index = len(stack)-1
    print("TOP OF THE STACK")
    while (index >=0):
        print(f"{index} Item ---> bytes = {str(stack[index].hex())} ,  int = {str(int.from_bytes(stack[index], byteorder='big'))}")
        index-=1
    print("")

def print_memory(memory:bytearray):
    print("")
    index=0
    while (index < len(memory)-1):
        print(f"Memory location {index} ---> bytes = {memory[index:index+32].hex()} ")
        # print(f"memory length is {len(memory[index:index+32])}")
        index+=32
    print("")