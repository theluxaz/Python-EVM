from utils.utils import print_memory

# 0x51    MLOAD       Load word from memory
# 0x52    MSTORE      Save word to memory
# 0x53    MSTORE8     Save byte to memory
# 0x59    MSIZE       Get the size of active memory in bytes
word_length = 32


class Memory:
    bytes_array = bytearray(0)

    def __init__(self):
        print("INITIALIZING MEMORY")
        self.bytes_array = bytearray(0)

    def store(self, offset: int, value: bytearray):
        if len(self.bytes_array) + word_length > 2**256 - 1:
            raise Exception("Maximum memory reached!")
        processed_value = bytearray(value)
        length_needed = offset + word_length

        if length_needed > len(self.bytes_array):
            self.expand_memory(length_needed)

        processed_value.extend(bytearray(word_length - len(processed_value)))
        # enable with if statement if issues found
        # if(len(processed_value)<word_length):
        #     processed_value = processed_value.extend(bytearray(word_length-len(processed_value)))

        for index, byte in enumerate(processed_value):
            self.bytes_array[offset + index] = byte
        print_memory(self.bytes_array)
        return processed_value

    def store8(self, offset: int, value: bytearray) -> None:
        if len(self.bytes_array) + 1 > 2**256 - 1:
            raise Exception("Maximum memory reached!")
        length_needed = offset + 1
        if length_needed > len(self.bytes_array):
            self.expand_memory(length_needed)

        for index, byte in enumerate(value):
            self.bytes_array[offset + index] = byte
        print_memory(self.bytes_array)
        return value

    def load(self, offset: int, size: int) -> bytes:
        length_needed = offset + size
        if length_needed > len(self.bytes_array):
            self.expand_memory(length_needed)
        result = self.bytes_array[offset : offset + size]
        print_memory(self.bytes_array)
        return result

    def expand_memory(self, length_needed: int):
        extend_to_number = ((length_needed) - len(self.bytes_array)) + (
            (word_length - ((length_needed - len(self.bytes_array)))) % word_length
        )
        self.bytes_array.extend(bytearray(extend_to_number))

    def size(self) -> None:
        print(f"Byte array is {len(self.bytes_array)}")
        return len(self.bytes_array)
