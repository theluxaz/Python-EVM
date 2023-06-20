from executor import Executor
from opcode_list import opcodes_list


# hexcode = "6001600201"

#Testing if memory works
hexcode = "60256000526020600051"

def main(bytecode: bytearray ) -> None:
    #Runs code
    executor = Executor(bytecode=bytecode,opcodes_list= opcodes_list)
    executor.run()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))