from executor import Executor
from opcode_list import opcodes_list


hexcode = "5a6000600957600160055b5a6003"
starting_gas = 40000


def main(bytecode: bytearray ) -> None:
    #Runs code
    executor = Executor(bytecode=bytecode,opcodes_list= opcodes_list,starting_gas=starting_gas)
    executor.run()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))