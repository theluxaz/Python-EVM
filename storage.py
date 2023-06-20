
# class Item:
#     key:bytes(32)
#     value:bytes(32)

class Storage:
    storage = {}
    max_size_bytes = 32

    def store(self, key: bytearray, value:bytearray):
            self.storage[key] = value

    def load(self, key: bytearray) -> bytes:
        result = self.storage[key]
        print(result)
        return result