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
            print("") 
            instruction = self.get_next_opcode()
            if (self.pc > len(self.bytecode)):
                print("STOPPING RUNTIME - CODE FINISHED")
                print()
                return "Stopped"
            elif (instruction["name"]== "STOP"):
                print("STOPPING RUNTIME - STOP COMMAND")
                print()
                return "Stopped"
            print(f"Opcode Instruction  is : {instruction}")

            processing_function = self.instructions.get_instruction_function(instruction["name"])
            result = processing_function()

            self.instructions.stack.print()
            
            if(type(result) == int):
                print(f"Processing result is : int {result}")
            else:
                print(f"Processing result is : bytes {result.hex()}")
            print("--")   


    def process_bytecode(self, next_word) -> bytes:
        item = self.bytecode[self.pc : self.pc + next_word]
        self.pc += next_word
        return item
    
    def get_next_opcode(self):
        mnemonic = self.process_bytecode(1)
        opcode = [x for x in self.opcodes_list if x['mnemonic'] == int.from_bytes(mnemonic, byteorder="big")][0]
        return opcode
    


