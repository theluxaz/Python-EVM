
from collections import deque
from typing import (
    Union
)

class Stack:
    
    stack = None
    max_size = 1024
    #item = 32 bytes 

    def __init__(self):
        self.stack = deque()

    def push(self,item):
        self.stack.append(item)
        print(str(self.stack))
        print(self.stack[0])
        print(type(self.stack[0]))
        return item

    def pop(self) -> Union[int, bytes]:
        return self.stack.pop()
    
    #Duplicate
    def duplicate(self,offset:int):
        item = self.stack[len(self.stack) - offset]
        self.stack.append(item)  
        print(str(self.stack))
        return item

    #Swap
    def swap(self,offset:int):
        swap_index = (len(self.stack) -1 - offset)
        item_to_top = self.stack[swap_index]
        item_to_swap = self.pop()
        
        self.stack.append(item_to_top)
        del self.stack[swap_index]
        self.stack.insert((len(self.stack) - offset), item_to_swap)
        print(str(self.stack))
        return item_to_top
