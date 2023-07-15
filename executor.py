from stack import Stack
from memory import Memory
from instructions import Instructions
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from opcode_list import opcodes_list

class Executor:

    def __init__(self,contract_instance, bytecode:bytearray,execution_context:ExecutionContext,transaction_context:TransactionContext) -> None:
        self.contract_instance = contract_instance
        self.instructions = Instructions(self)
        self.bytecode = bytecode
        self.execution_context=execution_context
        self.transaction_context=transaction_context
        self.address = execution_context.self_address
        self.gas_remaining = transaction_context.gas
        self.gas_starting = transaction_context.gas
        self.logs = []
        self.pc = 0
        self.stopped = False
        self.reverted = False
        self.returned = False
        self.invalid = False

    #main processing loop
    def run(self):
        while not self.stopped and not self.reverted and not self.returned:
            print("") 
            instruction = self.get_next_opcode()
            self.gas_remaining = self.gas_remaining - instruction["gas"]
            if (self.pc > len(self.bytecode)):
                print("STOPPING RUNTIME - CODE FINISHED")
                print()
                self.stopped == True
                return "STOPPED"
            # elif (instruction["name"]== "STOP"):
            #     print("STOPPING RUNTIME - STOP COMMAND")
            #     print()
            #     self.stopped == True
            #     return "Stopped"
            #TODO ADD PROPER GAS ERRORS
            elif (self.gas_remaining < 0):
                print("STOPPING RUNTIME - OUT OF GAS")
                print()
                self.stopped == True
                return "STOPPED"
            print(f"Opcode Instruction  is : {instruction}")

            processing_function = self.instructions.get_instruction_function(instruction["name"])
            result = processing_function()

            self.instructions.stack.print()
            
            if(self.returned):
                return result
            elif(self.reverted):
                #TODO IMPLEMENT REVERT FUNCTIONALITY
                return "REVERT"
            elif(self.stopped):
                #TODO IMPLEMENT STOPPED FUNCTIONALITY
                return "STOPPED"
            elif(self.invalid):
                #TODO IMPLEMENT INVALID FUNCTIONALITY
                return "INVALID"
            
            print(result)
            if(result):
                if(type(result) == int):
                    print(f"Processing result is : int {result}")
                else:
                    print(f"Processing result is : bytes {result.hex()}")
            print(f"Gas remaining: {self.gas_remaining} / {self.gas_starting}")
            print("--")   

    #main processing loop
    def run_testing(self):
        while not self.stopped and not self.reverted and not self.returned:
            print("") 
            instruction = self.get_next_opcode()
            self.gas_remaining = self.gas_remaining - instruction["gas"]
            if (self.pc > len(self.bytecode)):
                print("STOPPING RUNTIME - CODE FINISHED")
                print()
                self.stopped == True
                return "STOPPED"
            # elif (instruction["name"]== "STOP"):
            #     print("STOPPING RUNTIME - STOP COMMAND")
            #     print()
            #     self.stopped == True
            #     return "STOPPED"
            #TODO ADD PROPER GAS ERRORS
            elif (self.gas_remaining < 0):
                print("STOPPING RUNTIME - OUT OF GAS")
                print()
                self.stopped == True
                return "STOPPED"
            print(f"Opcode Instruction  is : {instruction}")

            processing_function = self.instructions.get_instruction_function(instruction["name"])
            result = processing_function()

            self.instructions.stack.print()
            
            if(self.returned):
                return result
            elif(self.reverted):
                #TODO IMPLEMENT REVERT FUNCTIONALITY
                return "REVERT"
            elif(self.stopped):
                #TODO IMPLEMENT STOPPED FUNCTIONALITY
                print("stop actuator")
                return "STOPPED"
            elif(self.invalid):
                #TODO IMPLEMENT INVALID FUNCTIONALITY
                return "INVALID"
            
            print(result)
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
        if(offset >= len(self.bytecode)):
            return None
        mnemonic = self.bytecode[offset : offset+1]
        print(str(self.bytecode))
        print(f"Byte offset at {offset} is {mnemonic} or mnemonic {int.from_bytes(mnemonic, byteorder='big')} pc is {self.pc}, len of bytecode is {len(self.bytecode)}")
        opcode = [x for x in opcodes_list if x['mnemonic'] == int.from_bytes(mnemonic, byteorder="big")][0]
        return opcode
    
    def set_pc(self,pc):
        self.pc = pc
        return pc
    
    def print_logs(self):
        for log in self.logs:
            print(f"Log: account={log['account']}   topics={get_bytearray_list_to_string(log['topics'])}   data={log['data'].hex()}")
    
    #Chekcs if the jump destination is a value used by push and not opcode instruction
    def is_opcode_valid(self,jump_target_position):
        for i in range(1,32):
            mnemonic = self.bytecode[jump_target_position-i : jump_target_position+1-i]
            opcode = [x for x in opcodes_list if x['mnemonic'] == int.from_bytes(mnemonic, byteorder="big")]
            if(opcode):
                opcode = opcode[0]
                #Check if PUSH was previously and number unusable
                if "PUSH"+str(i) == opcode["name"]:
                    return False
            
        return True
        
                
def get_bytearray_list_to_string(data_array):
    result = ""
    for item in data_array:
        if(len(result) >1):
            result += ", "
        result += item.hex()
    return result
    



