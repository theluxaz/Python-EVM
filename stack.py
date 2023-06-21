
from collections import deque
from typing import (
    Union
)
from utils import print_deque

class Stack:
    
    stack = None
    max_size = 1024
    #item = 32 bytes 

    def __init__(self):
        self.stack = deque()

    def push_bytes(self,item):
        self.stack.append(item)
        return item
    
    def push_int(self,item):
        item = item.to_bytes((item.bit_length() + 7) // 8, byteorder = 'big')
        self.stack.append(item)
        return item

    def pop_bytes(self) -> bytes:
        popped = self.stack.pop()
        return popped
    
    def pop_int(self) -> int:
        popped = int.from_bytes(self.stack.pop(),byteorder="big")
        return popped
    
    #Duplicate
    def duplicate(self,offset:int):
        item = self.stack[len(self.stack) - offset]
        self.stack.append(item)  
        return item

    #Swap
    def swap(self,offset:int):
        swap_index = (len(self.stack) -1 - offset)
        item_to_top = self.stack[swap_index]
        item_to_swap = self.pop()
        
        self.stack.append(item_to_top)
        del self.stack[swap_index]
        self.stack.insert((len(self.stack) - offset), item_to_swap)
        return item_to_top
    
    #Swap
    def print(self):
        print_deque(self.stack)
