

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
        return value

    def store8(self, offset: int, value:int) -> None:
        word_length = 32

        #TODO refactor
        #expand memory
        if((offset+word_length) > len(self.bytes_array)):
            print("extending")
            self.bytes_array.extend(bytearray((offset+word_length)-len(self.bytes_array)))
            print(self.bytes_array)
             
        print(offset)
        print(type(offset))
        # self.bytes_array[:offset] + value + self.bytes_array[offset][offset + 1:]
        self.bytes_array[offset] = value
        return value

    def load(self, offset: int, size:int) -> bytes:
        # try memoryview() ??
        result = self.bytes_array[offset : offset + size]
        print(result)
        return result

    def size(self) -> None:
        print(f"Byte array is {len(self.bytes_array)}")
        return len(self.bytes_array)