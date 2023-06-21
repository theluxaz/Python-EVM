from collections import deque

def unsigned_to_signed(value: int) -> int:
    if value <= (2**256 - 1):
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