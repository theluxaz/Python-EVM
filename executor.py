from stack import Stack
from memory import Memory
from opcodes import Opcodes




class Executor:

    def __init__(self, bytecode:bytearray,opcodes_list:list) -> None:
        self.stack = Stack()
        self.memory = Memory()
        self.bytecode = bytecode
        self.pc = 0
        self.stopped = False
        self.opcodes_list = opcodes_list
        self.opcodes_class = Opcodes()

    def processBytecode(self, next_word) -> int:
        item = int.from_bytes(self.bytecode[self.pc : self.pc + next_word], byteorder="big")
        
        # print(".")
        # print(len(self.bytecode))
        # print(str(item))

        self.pc += next_word
        print("PC is "+str(self.pc))
        return item
    
    def getOpcode(self):
        mnemonic = self.processBytecode(1)
        opcode = [x for x in self.opcodes_list if x['mnemonic'] == mnemonic]
        return opcode
    
    def getMethod(self,opcode_name:str):
        method = None
        try:
            method = getattr(self.opcodes_class, opcode_name)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(self.opcodes_class.__class__.__name__, opcode_name))
        return method

