
# class Item:
#     key:bytes(32)
#     value:bytes(32)

class Storage:
    storage = {}
    max_size_bytes = 32
    
    def __init__(self) :
        print("INITIALIZING STORAGE ----------------------------------------------")
        self.storage = {}

    def store(self, key: int, value:int):
        self.storage[key] = value
        print(f"Storage: {self.storage}")
        return value

    def load(self, key: int) -> bytes:
        result = self.storage.get(key)
        print(f"Storage: {self.storage}")
        print(f"Retrieved value: {result}")
        return result