
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

    def pop(self) -> Union[int, bytes]:
        return self.stack.pop()
    
    #Duplicate
    def dup(self,offset:int):
        self.stack.append(self.stack(len(self._items)- 1 - self.stack(offset)))

    #Swap
    def swap(self,offset:int):
        item_to_top = self.stack[(len(self._items)- 1 - self.stack(offset))]
        item_to_swap = self.pop()
        self.stack.append(item_to_top)
        self.stack.insert((len(self._items)- 1 - self.stack(offset)), item_to_swap)
