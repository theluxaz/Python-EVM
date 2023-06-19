

# 0x51    MLOAD       Load word from memory
# 0x52    MSTORE      Save word to memory
# 0x53    MSTORE8     Save byte to memory
# 0x59    MSIZE       Get the size of active memory in bytes

class Memory:
    bytes_array = bytearray(0)


    def store(self, offset: int, size:int, value:bytes) -> None:
        return None

    def store8(self, offset: int, size:int, value:bytes) -> None:
        return None

    def load(self, offset: int, size:int) -> bytes:
        return None

    def size(self) -> None:
        print(f"Byte array is f{len(bytearray)}")
        return len(bytearray)