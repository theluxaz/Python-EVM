from executor import Executor
from opcode_list import opcodes_list


# hexcode = "6001600201"

# #Testing if memory works
# hexcode = "60256000526020600051"

# #Testing if storage works
# hexcode = "60426000556020600054"

# #Testing if DUP and SWAP works
# hexcode = "6009600580829092"

#Testing if PUSH works properly (adds address to stack)
hexcode = "600b6005808273dbc05b1ecb4fdaef943819c0b04e9ef6df4babd69092"

def main(bytecode: bytearray ) -> None:
    #Runs code
    executor = Executor(bytecode=bytecode,opcodes_list= opcodes_list)
    executor.run()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))