from stack import Stack
from memory import Memory
from instructions import Instructions




class Executor:

    def __init__(self, bytecode:bytearray,opcodes_list:list) -> None:
        self.instructions = Instructions(self)
        self.bytecode = bytecode
        self.opcodes_list = opcodes_list
        self.pc = 0
        self.stopped = False

    #main processing loop
    def run(self):
        while not self.stopped:
            instruction = self.getNextOpcode()
            if self.pc > len(self.bytecode):
                break
            print(f"Opcode Instruction  is : {instruction}")

            processing_function = self.instructions.getInstructionFunction(instruction[0]["name"])
            result = processing_function()
            print(f"Processing result is : {result}")
            
            # print(f"{instruction} @ pc={executor.pc}")
            # print(context)

            print("--")   


    def processBytecode(self, next_word) -> int:
        item = int.from_bytes(self.bytecode[self.pc : self.pc + next_word], byteorder="big")
        
        # print(".")
        # print(len(self.bytecode))
        # print(str(item))

        self.pc += next_word
        print("PC is "+str(self.pc))
        return item
    
    def getNextOpcode(self):
        mnemonic = self.processBytecode(1)
        opcode = [x for x in self.opcodes_list if x['mnemonic'] == mnemonic]
        return opcode
    


