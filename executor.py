from stack import Stack
from memory import Memory
from instructions import Instructions
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from opcode_list import opcodes_list

class Executor:

    def __init__(self, bytecode:bytearray,execution_context:ExecutionContext,transaction_context:TransactionContext) -> None:
        self.instructions = Instructions(self)
        self.bytecode = bytecode
        self.execution_context=execution_context
        self.transaction_context=transaction_context
        self.gas_remaining = transaction_context.gas
        self.gas_starting = transaction_context.gas
        self.pc = 0
        self.stopped = False

    #main processing loop
    def run(self):
        while not self.stopped:
            print("") 
            instruction = self.get_next_opcode()
            self.gas_remaining = self.gas_remaining - instruction["gas"]
            if (self.pc > len(self.bytecode)):
                print("STOPPING RUNTIME - CODE FINISHED")
                print()
                return "Stopped"
            elif (instruction["name"]== "STOP"):
                print("STOPPING RUNTIME - STOP COMMAND")
                print()
                return "Stopped"
            elif (self.gas_remaining < 0):
                print("STOPPING RUNTIME - OUT OF GAS")
                print()
                return "Stopped"
            print(f"Opcode Instruction  is : {instruction}")

            processing_function = self.instructions.get_instruction_function(instruction["name"])
            result = processing_function()

            self.instructions.stack.print()
            if(result):
                if(type(result) == int):
                    print(f"Processing result is : int {result}")
                else:
                    print(f"Processing result is : bytes {result.hex()}")
            print(f"Gas remaining: {self.gas_remaining} / {self.gas_starting}")
            print("--")   


    def process_bytecode(self, next_word) -> bytes:
        item = self.bytecode[self.pc : self.pc + next_word]
        self.pc += next_word
        return item
    
    def get_next_opcode(self):
        mnemonic = self.process_bytecode(1)
        opcode = [x for x in opcodes_list if x['mnemonic'] == int.from_bytes(mnemonic, byteorder="big")][0]
        return opcode
    
    def check_opcode_at_pc(self,offset):
        mnemonic = self.bytecode[offset : offset+1]
        opcode = [x for x in opcodes_list if x['mnemonic'] == int.from_bytes(mnemonic, byteorder="big")][0]
        return opcode
    
    def set_pc(self,pc):
        self.pc = pc
        return pc
    


