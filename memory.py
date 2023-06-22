from utils import print_memory

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
                self.bytes_array[offset + index] = byte
        print_memory(self.bytes_array)
        return value

    def store8(self, offset: int, value:int) -> None:
        word_length = 32

        #TODO refactor
        #expand memory
        if((offset+word_length) > len(self.bytes_array)):
            print("extending")
            self.bytes_array.extend(bytearray((offset+word_length)-len(self.bytes_array)))
            print(self.bytes_array)
             
        self.bytes_array[offset] = value
        print_memory(self.bytes_array)
        return value

    def load(self, offset: int, size:int) -> bytes:
        # try memoryview() ??
        result = self.bytes_array[offset : offset + size]
        return result

    def size(self) -> None:
        print(f"Byte array is {len(self.bytes_array)}")
        return len(self.bytes_array)