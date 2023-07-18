from typing import Optional


class Storage:
    storage = {}
    max_size_bytes = 32
    
    def __init__(self,storage:Optional[dict] = None) :
        if(storage):
            print("REMAKING STORAGE")
            print(type(storage))
            self.storage = storage

    def store(self, key: int, value:int):
        print(f"Storage: {self.storage}")
        self.storage[key] = value
        print(f"Storage: {self.storage}")
        return value

    def load(self, key: int) -> bytes:
        result = self.storage.get(key)
        print(f"Storage: {self.storage}")
        print(f"Retrieved value: {result}")
        return result