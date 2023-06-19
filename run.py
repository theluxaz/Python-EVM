from executor import Executor
from opcode_list import opcodes_list
from opcodes import Opcodes


hexcode = "6001600201"

def main(bytecode: bytearray ) -> None:
    #Runs code
    executor = Executor(bytecode=bytecode,opcodes_list= opcodes_list)

    while not executor.stopped:
        pc = executor.pc
        result = executor.getOpcode()
        if executor.pc > len(executor.bytecode):
            break
        print(result)
        processing_function = executor.getMethod(result[0]["name"])
        result = processing_function(executor)
        print(result)
        
        

        # print(f"{instruction} @ pc={pc}")
        # print(context)
        # print()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))