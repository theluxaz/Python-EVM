from stack import Stack
from memory import Memory
from storage import Storage
from utils import signed_to_unsigned,unsigned_to_signed
from eth_hash.auto import keccak

max_value = 2**256 - 1
max_ceiling = 2**256 

class Instructions:

    def __init__(self,executor:object) -> None:
        self.stack = Stack()
        self.memory = Memory()
        self.storage = Storage()
        self.executor = executor

    def get_instruction_function(self,opcode_name:str):
        method = None
        try:
            method = getattr(self, opcode_name)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(self.opcodes_class.__class__.__name__, opcode_name))
        return method    





    #OPCODE     GAS
    #00         0  
    def STOP(self):
        print("Execution stopped")
        self.executor.stopped = True



    #Arithmetic Opcodes

    #OPCODE     GAS
    #01         3  
    def ADD(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        return self.stack.push_int(a+b) #possibly add this on this line  & max_value

    #OPCODE     GAS
    #02         5  
    def MUL(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        return self.stack.push_int(a*b) #possibly add this on this line  & max_value

    #OPCODE     GAS
    #03         3  
    def SUB(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        return self.stack.push_int(a-b) #possibly add this on this line  & max_value

    #OPCODE     GAS
    #04         2  
    def DIV(self) -> int:
        #(a:int, b:int)
        num = self.stack.pop_int()
        den = self.stack.pop_int()

        if den == 0:
            return self.stack.push_int(0)
        else:
            return self.stack.push_int(num//den) #possibly add this on this line  & max_value

    #OPCODE     GAS
    #05         5  
    def SDIV(self) -> int:
        #(a:int, b:int)
        #SIGNED INTEGER DIVISION
        a = self.stack.pop_int()
        b = self.stack.pop_int()

        num = unsigned_to_signed(a)
        den = unsigned_to_signed(b)

        
        pos_or_neg = -1 if num * den < 0 else 1

        if den == 0:
            result = 0
        else:
            result = pos_or_neg * (abs(num) // abs(den))

        return self.stack.push_int(signed_to_unsigned(result)) #possibly add this on this line  & max_value

    #OPCODE     GAS
    #06         5  
    def MOD(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop_int()
        b = self.stack.pop_int()

        if(b==0):
            return self.stack.push_int(0)
        else:
            return self.stack.push_int(a%b)

    #OPCODE     GAS
    #07         5  
    def SMOD(self) -> int:
        #(a:int, b:int)
        #SIGNED MODULUS
        a = self.stack.pop_int()
        b = self.stack.pop_int()

        val = unsigned_to_signed(a)
        mod = unsigned_to_signed(b)

        pos_or_neg = -1 if val < 0 else 1

        if mod == 0:
            result = 0
        else:
            result = (abs(val) % abs(mod) * pos_or_neg) #possibly add this on this line  & max_value

        return self.stack.push_int(signed_to_unsigned(result))


    #OPCODE     GAS
    #08         8  
    def ADDMOD(self) -> int:
        #(a:int, b:int, n:int
        #ADD TWO VALUES, THEN MODULUS
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        n = self.stack.pop_int()

        if(n==0):
            return self.stack.push_int(0)
        else:
            return self.stack.push_int((a+b)%n)

    #OPCODE     GAS
    #09         8  
    def MULMOD(self) -> int:
        #(a:int, b:int, n:int
        #MULTIPLY TWO VALUES, THEN MODULUS
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        n = self.stack.pop_int()

        if(n==0):
            return self.stack.push_int(0)
        else:
            return self.stack.push_int((a*b)%n)

    #OPCODE     GAS
    #0A         10   dynamic  
    def EXP(self) -> int:
        #(a:int (base), exponent:int
        #EXPONENT
        a = self.stack.pop_int()
        exponent = self.stack.pop_int()

        if(exponent ==0):
            return self.stack.push_int(1)
        elif(a==1):
            return self.stack.push_int(0)
        else:
            #TODO  ADD MODULUS? (3rd parameter in .pow) -> max_ceiling
            return self.stack.push_int(pow(a,exponent)) 



    #OPCODE     GAS
    #0B         5  
    def SIGNEXTEND(self) -> int:
        #(b:int (bits), x:int (value)
        #Extend length of two’s complement signed integer

        #official implementation

        b = self.stack.pop_int()
        x = self.stack.pop_int()

        if b < 32:
            testbit = b * 8 + 7
            sign_bit = 1 << testbit
            if x & sign_bit:
                result = x | (max_ceiling - sign_bit)
            else:
                result = x & (sign_bit - 1)
        else:
            result = x
        return self.stack.push_int(result)







    #Comparison & Bitwise Logic Operations


    #OPCODE     GAS
    #10         3  
    def LT(self) -> int:
        #LESS THAN
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        return self.stack.push_int(int(a<b))

    #OPCODE     GAS
    #11         3  
    def GT(self) -> int:
        #GREATER THAN
        a = self.stack.pop_int()
        b = self.stack.pop_int()
        return self.stack.push_int(int(a>b))

    #OPCODE     GAS
    #12         3  
    def SLT(self) -> int:
        #SIGNED LESS THAN
        a = unsigned_to_signed(self.stack.pop_int())
        b = unsigned_to_signed(self.stack.pop_int())
        return self.stack.push_int(signed_to_unsigned(int(a<b)))

    #OPCODE     GAS
    #13         3  
    def SGT(self) -> int:
        #SIGNED GREATER THAN
        a = unsigned_to_signed(self.stack.pop_int())
        b = unsigned_to_signed(self.stack.pop_int())
        return self.stack.push_int(signed_to_unsigned(int(a>b)))

    #OPCODE     GAS
    #14         3  
    def EQ(self) -> int:
        #EQUAL
        a = self.stack.pop_bytes()
        b = self.stack.pop_bytes()
        return self.stack.push_int(int(a==b))

    #OPCODE     GAS
    #15         3  
    def ISZERO(self) -> int:
        a = self.stack.pop_int()
        return self.stack.push_int(int(a==0))

    #OPCODE     GAS
    #16         3  
    def AND(self) -> bytearray: #TODO figure out return type
        #BITWISE AND
        item1 = self.stack.pop_int()
        item2 = self.stack.pop_int()
        return self.stack.push_int(item1 & item2)


    #OPCODE     GAS
    #17         3  
    def OR(self) -> bytearray: #TODO figure out return type
        #BITWISE OR
        item1 = self.stack.pop_int()
        item2 = self.stack.pop_int()
        return self.stack.push_int(item1 | item2)

    #OPCODE     GAS
    #18         3  
    def XOR(self) -> bytearray: #TODO figure out return type
        #BITWISE XOR
        item1 = self.stack.pop_int()
        item2 = self.stack.pop_int()
        return self.stack.push_int(item1 ^ item2)

    #OPCODE     GAS
    #19         3  
    def NOT(self) -> bytearray: #TODO figure out return type
        #BITWISE NOT
        #OR TRY
        item1 = self.stack.pop_int()
        return self.stack.push_int(max_value- item1)
        

    #OPCODE     GAS
    #1A         3  
    def BYTE(self)  -> int:
        #offset and byte value
        #(i:int (position),x:bytes (value))
        #RETRIEVE SINGLE BYTE FROM WORD
        pos = self.stack.pop_int()
        val = self.stack.pop_int()

        if pos >= 32:
            result = 0
        else:
            result = (val // pow(256, 31 - pos)) % 256

        return self.stack.push_int(result)

    #OPCODE     GAS
    #1B         3  
    def SHL(self)  -> bytes:
        #(shift:int (bits),value:bytes(value))
        #SHIFT shift VALUE value to the LEFT
        shift = self.stack.pop_int()
        val = self.stack.pop_int()
        if(shift> 255):
            return self.stack.push_int(0)

        return self.stack.push_int(val << shift)

    #OPCODE     GAS
    #1C         3  
    def SHR(self) -> bytes:
        #(shift:int (bits),value:bytes(value))
        #SHIFT shift VALUE value to the RIGHT
        shift = self.stack.pop_int()
        val = self.stack.pop_int()
        if(shift> 255):
            return self.stack.push_int(0)

        return self.stack.push_int(val >> shift)

    #UNFINISHED  - More info: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-145.md
    # Implementation here from EIP https://github.com/ethereum/aleth/pull/4054/files
    #OPCODE     GAS
    #1D         3  
    def SAR(self)  -> bytes:
        #SHIFT shift VALUE value to the RIGHT
        #(shift:int,value:bytes) --- IS SIGNED, similar to previous
        #Shift the bits towards the least significant one. The bits moved before the first one are discarded, 
        #the new bits are set to 0 if the previous most significant bit was 0, otherwise the new bits are set to 1.
        shift = self.stack.pop_int()
        val = self.stack.pop_int()
        if(shift> 255):
            return self.stack.push_int(0)
        
        return self.stack.push_int(val >> shift)






    # Test more, not too sure if correct
    #Sha3 Hashing Operations

    #OPCODE     GAS
    #20         30+   dynamic  
    def SHA3(self):
        #(offset:int,size:int)
        #Compute Keccak-256 hash
        offset = self.stack.pop_int()
        size = self.stack.pop_int()

        loaded_value = self.memory.load(offset, size)

        return self.stack.push_bytes(keccak(loaded_value))





    #Environmental Information

    #OPCODE     GAS
    #30         2 
    def ADDRESS(self):
        #gets address of current execution account
        return None

    #OPCODE     GAS
    #31         100 hot 3200 cold  dynamic  
    def BALANCE(self):
        #Checks the balance of given address
        return None

    #OPCODE     GAS
    #32         2  
    def ORIGIN(self):
        #Get execution origination address
        return self.stack.push_bytes(self.executor.transaction_context.origin_address)

    #OPCODE     GAS
    #33         2  
    def CALLER(self):
        #Get address of msg.sender
        return self.stack.push_bytes(self.executor.transaction_context.sender_address)

    #OPCODE     GAS
    #34         2  
    def CALLVALUE(self):
        #Get deposited value by the instruction/transaction responsible for this execution
        return self.stack.push_int(self.executor.transaction_context.value)

    #TODO, CHECK IF WHOLE 32bit WORD SHOULD BE RETURNED
    #OPCODE     GAS
    #35         3  
    def CALLDATALOAD(self):
        #byte offset i, Get input data of calldata
        offset = self.stack.pop_int()
        word_length=32
        return self.stack.push_bytes(self.executor.transaction_context.data[offset : offset + word_length])

    #OPCODE     GAS
    #36         2  
    def CALLDATASIZE(self):
        #Get size of input data of calldata
        return self.stack.push_int(len(self.executor.transaction_context.data))


    #OPCODE     GAS
    #37         3 dynamic
    def CALLDATACOPY(self):
        #Copy input data in calldata to memory
        #(self,dest_offset:int, offset:int,size:int)
        mem_offset = self.stack.pop_int()
        calldata_offset = self.stack.pop_int()
        size = self.stack.pop_int()

        return self.memory.store(mem_offset,self.executor.transaction_context.data[calldata_offset : calldata_offset + size])

    #OPCODE     GAS
    #38         2  
    def CODESIZE(self) -> int:
        #Get size of code running in current environment
        return self.stack.push_int(len(self.executor.bytecode))

    #OPCODE     GAS
    #39         3 dynamic
    def CODECOPY(self):
        #Copy code running in current environment to memory
        #(self,dest_offset:int, offset:int,size:int)
        mem_offset = self.stack.pop_int()
        bytecode_offset = self.stack.pop_int()
        size = self.stack.pop_int()
        return self.memory.store(mem_offset,self.executor.bytecode[bytecode_offset : bytecode_offset + size])
        

    #OPCODE     GAS
    #3A         2  
    def GASPRICE(self):
        #Get price of gas in current environment
        return self.stack.push_int(self.executor.transaction_context.gas_price)

    #OPCODE     GAS
    #3B         100 dynamic  
    def EXTCODESIZE(self):
        #Get size of an account’s code
        address = self.stack.pop_int()
        if(address):
            return self.stack.push_int(len(bytearray.fromhex(self.executor.execution_context.external_contracts[address])))
        else:
            return self.stack.push_int(0)
        
    #OPCODE     GAS
    #3C         100 dynamic  
    def EXTCODECOPY(self):
        #Copy an account’s code to memory
        #(self,addressbytes,dest_offset:int, offset:int,size:int)
        address = self.stack.pop_int()
        mem_offset = self.stack.pop_int()
        bytecode_offset = self.stack.pop_int()
        size = self.stack.pop_int()
        if(address):
            return self.memory.store(mem_offset,bytearray.fromhex(self.executor.execution_context.external_contracts[address][bytecode_offset : bytecode_offset + size]))
        else:
            return self.stack.push_int(0)


    #OPCODE     GAS
    #3D         2  
    def RETURNDATASIZE(self) -> int:
        #Get size of output data from the previous call from the current environment
        return None

    #OPCODE     GAS
    #3E         3  dynamic
    def RETURNDATACOPY(self,dest_offset:int, offset:int,size:int):
        #Copy output data from the previous call to memory
        return None

    #OPCODE     GAS
    #3F         100 dynamic  
    def EXTCODEHASH(self):
        #Get hash of an account’s code
        address = self.stack.pop_int()
        if(address):
            hashed_value = keccak(bytearray.fromhex(self.executor.execution_context.external_contracts[address]))
            return self.stack.push_bytes(hashed_value)
        else:
            return self.stack.push_int(0)






    #Block Information

    #NOT DONE - IMPLEMENT HASH HISTORY LATER
    #OPCODE     GAS
    #40         20 
    def BLOCKHASH(self):
        #Get the hash of one of the 256 most recent complete blocks
        offset = self.stack.pop_int()
        if(offset < 0 or offset >= 256):
            return self.stack.push_int(0)
        return self.stack.push_bytes(self.executor.execution_context.block_hash)

    #OPCODE     GAS
    #41         2
    def COINBASE(self):
        #Get the block’s beneficiary address (miner, proposer)
        return self.stack.push_bytes(self.executor.execution_context.coinbase)

    #OPCODE     GAS
    #42         2  
    def TIMESTAMP(self):
        #Get the block’s timestamp
        return self.stack.push_int(self.executor.execution_context.timestamp)

    #OPCODE     GAS
    #43         2  
    def NUMBER(self):
        #Get the block’s number
        return self.stack.push_int(self.executor.execution_context.block_number)

    #OPCODE     GAS
    #44         2  
    def DIFFICULTY(self):
        #Get the block’s difficulty
        return self.stack.push_int(self.executor.execution_context.block_difficulty)

    #OPCODE     GAS
    #45         2  
    def GASLIMIT(self):
        #Get the block’s gas limit
        return self.stack.push_int(self.executor.execution_context.gas_limit)

    #OPCODE     GAS
    #46         2  
    def CHAINID(self):
        #Get the chain ID
        return self.stack.push_int(self.executor.execution_context.chain_id)


    #OPCODE     GAS
    #47         5
    def SELFBALANCE(self):
        #Get balance of currently executing account
        return self.stack.push_int(self.executor.execution_context.self_balance)

    #OPCODE     GAS
    #48         2  
    def BASEFEE(self):
        #Get the base fee
        return self.stack.push_int(self.executor.execution_context.base_fee)







    #Stack, Memory, Storage and Flow Operations


    #OPCODE     GAS
    #50         2 
    def POP(self):
        #Remove item from stack
        item = self.stack.pop_bytes()
        return item

    #OPCODE     GAS
    #51         3 dynamic  
    def MLOAD(self) -> bytes:
        #Load word from memory
        offset = self.stack.pop_int()
        size=32
        return self.stack.push_bytes(self.memory.load(offset,size))

    #TODO - STORE BYTES OR INT IN STACK?? CHECK CONVERSION FROM BYTES with .to_bytes
    #OPCODE     GAS
    #52         3 dynamic    
    def MSTORE(self):
        #Save word to memory
        offset = self.stack.pop_int()
        value = self.stack.pop_int()

        processed_value = value.to_bytes(32, 'big')
        
        print(f"Normal value {value}")
        # length = len(value) % 32
        # if length > 0:
        #     value += bytes(32 - length)
        print(f"Processed value {processed_value}")

        return self.memory.store(offset,processed_value)

    #TODO add validation!!!
    #OPCODE     GAS
    #53         3 dynamic    
    def MSTORE8(self):
        #Save word to memory
        offset = self.stack.pop_int()
        value = self.stack.pop_int()

        return self.memory.store8(offset,value)

    #OPCODE     GAS
    #54         100 dynamic    
    def SLOAD(self) -> int:
        #Load word from storage
        key = self.stack.pop_int()

        # processed_key = key.to_bytes(32, 'big')

        return self.stack.push_int(self.storage.load(key))

    #OPCODE     GAS
    #55         100 dynamic  
    def SSTORE(self):
        #Save word to storage
        key = self.stack.pop_int()
        value = self.stack.pop_int()
        #delete later
        # processed_key = key.to_bytes(32, 'big')
        # processed_value = value.to_bytes(32, 'big')

        return self.storage.store(key,value)


    #OPCODE     GAS
    #56         8  
    def JUMP(self):
        #Alter the program counter
        offset = self.stack.pop_int()
        print(f"JUMPDEST {offset}")
        next_opcode = self.executor.check_opcode_at_pc(offset)
        print(f"NEXT OPCODE {next_opcode}")
        if(next_opcode and next_opcode["name"]== "JUMPDEST"):
            self.executor.set_pc(offset)
            print("good destination")
            return offset
        else:
            print("Revert")
            return "STOPPED"


    #OPCODE     GAS
    #57         10
    def JUMPI(self):
        #Conditionally alter the program counter
        offset = self.stack.pop_int()
        condition = self.stack.pop_int()
        print(f"JUMPDEST {offset}")
        next_opcode = self.executor.check_opcode_at_pc(offset)
        print(f"NEXT OPCODE {next_opcode}")
        if(condition):
            if(next_opcode and next_opcode["name"]== "JUMPDEST"):
                self.executor.set_pc(offset)
                print("good destination")
                return offset
            else:
                print("Revert")
                return "STOPPED"
        else:
            print("Jumping condition failed")
            return None

    #OPCODE     GAS
    #58         2  
    def PC(self) -> int:
        #Get the value of the program counter prior to the increment corresponding to this instruction
        return self.stack.push_int(self.executor.pc-1) 

    #OPCODE     GAS
    #59         2
    def MSIZE(self) -> int:
        #Get the size of active memory in bytes
        return self.stack.push_int(self.memory.size()) 
        

    #OPCODE     GAS
    #5A         2  
    def GAS(self) -> int:
        #Get the amount of available gas, including the corresponding reduction for the cost of this instruction
        return self.stack.push_int(self.executor.gas_remaining) 

    #OPCODE     GAS
    #5B         1 
    def JUMPDEST(self):
        #Mark a valid destination for jumpADD
        return None


    #OPCODE     GAS
    #5F         2   
    def PUSH0() -> int:
        #Place 0 bytes item on stack
        return 0





    # Push Operations

    #REFACTOR LATER
    #OPCODE     GAS
    #60         3   
    def PUSH1(self):
        #Place 1 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(1))

    #OPCODE     GAS
    #61         3   
    def PUSH2(self):
        #Place 2 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(2))

    #OPCODE     GAS
    #62         3   
    def PUSH3(self):
        #Place 3 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(3))

    #OPCODE     GAS
    #63         3   
    def PUSH4(self):
        #Place 4 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(4))

    #OPCODE     GAS
    #64         3   
    def PUSH5(self):
        #Place 5 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(5))

    #OPCODE     GAS
    #65         3   
    def PUSH6(self):
        #Place 6 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(6))

    #OPCODE     GAS
    #66         3   
    def PUSH7(self):
        #Place 7 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(7))

    #OPCODE     GAS
    #67         3   
    def PUSH8(self):
        #Place 8 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(8))

    #OPCODE     GAS
    #68         3   
    def PUSH9(self):
        #Place 9 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(9))

    #OPCODE     GAS
    #69         3   
    def PUSH10(self):
        #Place 10 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(10))

    #OPCODE     GAS
    #6A         3   
    def PUSH11(self):
        #Place 11 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(11))

    #OPCODE     GAS
    #6B         3   
    def PUSH12(self):
        #Place 12 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(12))

    #OPCODE     GAS
    #6C         3   
    def PUSH13(self):
        #Place 13 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(13))

    #OPCODE     GAS
    #6D         3   
    def PUSH14(self):
        #Place 14 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(14))

    #OPCODE     GAS
    #6E         3   
    def PUSH15(self):
        #Place 15 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(15))

    #OPCODE     GAS
    #6F         3   
    def PUSH16(self):
        #Place 16 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(16))


    #70s

    #OPCODE     GAS
    #70         3   
    def PUSH17(self):
        #Place 17 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(17))

    #OPCODE     GAS
    #71         3   
    def PUSH18(self):
        #Place 18 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(18))

    #OPCODE     GAS
    #72         3   
    def PUSH19(self):
        #Place 19 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(19))

    #OPCODE     GAS
    #73         3   
    def PUSH20(self):
        #Place 20 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(20))

    #OPCODE     GAS
    #74         3   
    def PUSH21(self):
        #Place 21 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(21))

    #OPCODE     GAS
    #75         3   
    def PUSH22(self):
        #Place 22 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(22))

    #OPCODE     GAS
    #76         3   
    def PUSH23(self):
        #Place 23 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(23))

    #OPCODE     GAS
    #77         3   
    def PUSH24(self):
        #Place 24 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(24))

    #OPCODE     GAS
    #78         3   
    def PUSH25(self):
        #Place 25 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(25))

    #OPCODE     GAS
    #79         3   
    def PUSH26(self):
        #Place 26 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(26))

    #OPCODE     GAS
    #7A         3   
    def PUSH27(self):
        #Place 27 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(27))

    #OPCODE     GAS
    #7B         3   
    def PUSH28(self):
        #Place 28 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(28))

    #OPCODE     GAS
    #7C         3   
    def PUSH29(self):
        #Place 29 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(29))

    #OPCODE     GAS
    #7D         3   
    def PUSH30(self):
        #Place 30 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(30))

    #OPCODE     GAS
    #7E         3   
    def PUSH31(self):
        #Place 31 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(31))

    #OPCODE     GAS
    #7F         3   
    def PUSH32(self):
        #Place 32 bytes item on stack
        return self.stack.push_bytes(self.executor.process_bytecode(32))






    #Duplication Operations


    #OPCODE     GAS
    #80         3   
    def DUP1(self):
        #Duplicate 1st stack item
        return self.stack.duplicate(1)

    #OPCODE     GAS
    #81         3   
    def DUP2(self):
        #Duplicate 2nd stack item
        return self.stack.duplicate(2)

    #OPCODE     GAS
    #82         3   
    def DUP3(self):
        #Duplicate 3rd stack item
        return self.stack.duplicate(3)

    #OPCODE     GAS
    #83         3   
    def DUP4(self):
        #Duplicate 4th stack item
        return self.stack.duplicate(4)

    #OPCODE     GAS
    #84         3   
    def DUP5(self):
        #Duplicate 5th stack item
        return self.stack.duplicate(5)

    #OPCODE     GAS
    #85         3   
    def DUP6(self):
        #Duplicate 6th stack item
        return self.stack.duplicate(6)

    #OPCODE     GAS
    #86         3   
    def DUP7(self):
        #Duplicate 7th stack item
        return self.stack.duplicate(7)

    #OPCODE     GAS
    #87         3   
    def DUP8(self):
        #Duplicate 8th stack item
        return self.stack.duplicate(8)

    #OPCODE     GAS
    #88         3   
    def DUP9(self):
        #Duplicate 9th stack item
        return self.stack.duplicate(9)

    #OPCODE     GAS
    #89         3   
    def DUP10(self):
        #Duplicate 10th stack item
        return self.stack.duplicate(10)

    #OPCODE     GAS
    #8A         3   
    def DUP11(self):
        #Duplicate 11th stack item
        return self.stack.duplicate(11)

    #OPCODE     GAS
    #8B         3   
    def DUP12(self):
        #Duplicate 12th stack item
        return self.stack.duplicate(12)

    #OPCODE     GAS
    #8C         3   
    def DUP13(self):
        #Duplicate 13th stack item
        return self.stack.duplicate(13)

    #OPCODE     GAS
    #8D         3   
    def DUP14(self):
        #Duplicate 14th stack item
        return self.stack.duplicate(14)

    #OPCODE     GAS
    #8E         3   
    def DUP15(self):
        #Duplicate 15th stack item
        return self.stack.duplicate(15)

    #OPCODE     GAS
    #8F         3   
    def DUP16(self):
        #Duplicate 16th stack item
        return self.stack.duplicate(16)









    #Exchange Operations


    #OPCODE     GAS
    #90         3   
    def SWAP1(self):
        #Exchange 1st and 2nd stack items
        return self.stack.swap(1)

    #OPCODE     GAS
    #91         3   
    def SWAP2(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 3rd stack items 
        return self.stack.swap(2)

    #OPCODE     GAS
    #92         3   
    def SWAP3(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 4th stack items
        return self.stack.swap(3)

    #OPCODE     GAS
    #93         3   
    def SWAP4(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 5th stack items
        return self.stack.swap(4)

    #OPCODE     GAS
    #94         3   
    def SWAP5(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 6th stack items
        return self.stack.swap(5)

    #OPCODE     GAS
    #95         3   
    def SWAP6(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 7th stack items
        return self.stack.swap(6)

    #OPCODE     GAS
    #96         3   
    def SWAP7(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 8th stack items
        return self.stack.swap(7)

    #OPCODE     GAS
    #97         3   
    def SWAP8(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 9th stack items
        return self.stack.swap(8)

    #OPCODE     GAS
    #98         3   
    def SWAP9(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 10th stack items
        return self.stack.swap(9)

    #OPCODE     GAS
    #99         3   
    def SWAP10(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 11th stack items
        return self.stack.swap(10)

    #OPCODE     GAS
    #9A         3   
    def SWAP11(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 12th stack items
        return self.stack.swap(11)

    #OPCODE     GAS
    #9B         3   
    def SWAP12(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 13th stack items
        return self.stack.swap(12)

    #OPCODE     GAS
    #9C         3   
    def SWAP13(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 14th stack items
        return self.stack.swap(13)

    #OPCODE     GAS
    #9D         3   
    def SWAP14(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 15th stack items
        return self.stack.swap(14)

    #OPCODE     GAS
    #9E         3   
    def SWAP15(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 16th stack items
        return self.stack.swap(15)

    #OPCODE     GAS
    #9F         3   
    def SWAP16(self):# ignored return types in the middle DO LATER
        #Exchange 1st and 17th stack items
        return self.stack.swap(16)






    # Logging Operations


    #OPCODE     GAS
    #A0         375 dynamic 
    def LOG0(offset:bytes,size:int):
        #Append log record with no topics
        return None

    #OPCODE     GAS
    #A1         750 dynamic 
    def LOG1(offset:bytes,size:int,topic1:bytes):
        #Append log record with 1 topic
        return None

    #OPCODE     GAS
    #A2         1125 dynamic   
    def LOG2(offset:bytes,size:int,topic1:bytes,topic2:bytes):
        #Append log record with 2 topics
        return None

    #OPCODE     GAS
    #A3         1500 dynamic   
    def LOG3(offset:bytes,size:int,topic1:bytes,topic2:bytes,topic3:bytes):
        #Append log record with 3 topics
        return None

    #OPCODE     GAS
    #A4         1875 dynamic   
    def LOG4(offset:bytes,size:int,topic1:bytes,topic2:bytes,topic3:bytes,topic4:bytes):
        #Append log record with 4 topics
        return None






    # System operations


    #OPCODE     GAS
    #F0         32000 dynamic   
    def CREATE(value:int,offset:bytes,size:int) -> bytes:
        #Create a new account with associated code
        return None

    #OPCODE     GAS
    #F1         100 dynamic   
    def CALL(gas:int,address:bytes,value:int,args_offset:bytes,args_size:int,ret_offset:bytes,ret_size:int) -> int:
        #Message-call into an account
        return None

    #OPCODE     GAS
    #F2         100 dynamic     
    def CALLCODE(gas:int,address:bytes,value:int,args_offset:bytes,args_size:int,ret_offset:bytes,ret_size:int) -> bytes:
        #Message-call into this account with alternative account’s code
        return None

    #OPCODE     GAS
    #F3         0 dynamic     
    def RETURN(offset:bytes,size:int) -> bytes:
        #Halt execution returning output data
        return None

    #OPCODE     GAS
    #F4         100 dynamic     
    def DELEGATECALL(gas:int,address:bytes,value:int,args_offset:bytes,args_size:int,ret_offset:bytes,ret_size:int) -> int:
        #Message-call into this account with an alternative account’s code, but persisting the current values for sender and value
        return None

    #OPCODE     GAS
    #F5         32000 dynamic     
    def CREATE2(value:int,offset:bytes,size:int,salt:bytes) -> bytes:
        #Create a new account with associated code at a predictable address
        return None

    #OPCODE     GAS
    #FA         100 dynamic     
    def STATICCALL(gas:int,address:bytes,value:int,args_offset:bytes,args_size:int,ret_offset:bytes,ret_size:int) -> int:
        #Static message-call into an account
        return None


    #OPCODE     GAS
    #FD         0 dynamic   
    def REVERT(self):
        #Halt execution reverting state changes but returning data and remaining gas
        return "Stopped"

    #OPCODE     GAS
    #FE         NaN dynamic  
    def INVALID(self) -> int:
        #Designated invalid instruction
        return "Stopped"

    #OPCODE     GAS
    #FF         5000 dynamic   
    def SELFDESTRUCT(address:bytes):
        #Halt execution and register account for later deletion
        return None 
        