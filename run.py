from executor import Executor
from opcode_list import opcodes_list


hexcode = "6000600957600160055b6003"


def main(bytecode: bytearray ) -> None:
    #Runs code
    executor = Executor(bytecode=bytecode,opcodes_list= opcodes_list)
    executor.run()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))