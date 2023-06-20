

# 0x51    MLOAD       Load word from memory
# 0x52    MSTORE      Save word to memory
# 0x53    MSTORE8     Save byte to memory
# 0x59    MSIZE       Get the size of active memory in bytes

class Memory:
    bytes_array = bytearray(0)


    def store(self, offset: int, value:bytearray):
        word_length = 32

        #TODO refactor
        #expand memory
        if((offset+word_length) > len(self.bytes_array)):
             self.bytes_array.extend(bytearray((offset+word_length)-len(self.bytes_array)))
             

        for index, byte in enumerate(value):
                print(f"index {index}")
                print(f"byte {byte}")
                self.bytes_array[offset + index] = byte
        return None

    def store8(self, offset: int, value:bytearray) -> None:
        word_length = 1

        #TODO refactor
        #expand memory
        if((offset+word_length) > len(self.bytes_array)):
             self.bytes_array.extend(bytearray((offset+word_length)-len(self.bytes_array)))
             

        self.bytes_array[offset] = value
        return None

    def load(self, offset: int, size:int) -> bytes:
        # try memoryview() ??
        result = self.bytes_array[offset : offset + size]
        print(result)
        return result

    def size(self) -> None:
        print(f"Byte array is f{len(bytearray)}")
        return len(bytearray)