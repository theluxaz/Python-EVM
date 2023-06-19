from stack import Stack
from memory import Memory
from utils import signed_to_unsigned,unsigned_to_signed

class Instructions:

    def __init__(self,executor:object) -> None:
        self.stack = Stack()
        self.memory = Memory()
        self.executor = executor

    def getInstructionFunction(self,opcode_name:str):
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
        a = self.stack.pop()
        b = self.stack.pop()
        return self.stack.push(a+b) #possibly add this on this line  & (2*256-1)

    #OPCODE     GAS
    #02         5  
    def MUL(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop()
        b = self.stack.pop()
        return self.stack.push(a*b) #possibly add this on this line  & (2*256-1)

    #OPCODE     GAS
    #03         3  
    def SUB(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop()
        b = self.stack.pop()
        return self.stack.push(a-b) #possibly add this on this line  & (2*256-1)

    #OPCODE     GAS
    #04         2  
    def DIV(self) -> int:
        #(a:int, b:int)
        num = self.stack.pop()
        den = self.stack.pop()

        if den == 0:
            return self.stack.push(0)
        else:
            return self.stack.push(num//den) #possibly add this on this line  & (2*256-1)

    #OPCODE     GAS
    #05         5  
    def SDIV(self) -> int:
        #(a:int, b:int)
        #SIGNED INTEGER DIVISION
        a = self.stack.pop()
        b = self.stack.pop()

        num = unsigned_to_signed(a)
        den = unsigned_to_signed(b)

        
        pos_or_neg = -1 if num * den < 0 else 1

        if den == 0:
            result = 0
        else:
            result = pos_or_neg * (abs(num) // abs(den))

        return self.stack.push(signed_to_unsigned(result)) #possibly add this on this line  & (2*256-1)

    #OPCODE     GAS
    #06         5  
    def MOD(self) -> int:
        #(a:int, b:int)
        a = self.stack.pop()
        b = self.stack.pop()

        if(b==0):
            return self.stack.push(0)
        else:
            return self.stack.push(a%b)

    #OPCODE     GAS
    #07         5  
    def SMOD(self) -> int:
        #(a:int, b:int)
        #SIGNED MODULUS
        a = self.stack.pop()
        b = self.stack.pop()

        val = unsigned_to_signed(a)
        mod = unsigned_to_signed(b)

        pos_or_neg = -1 if val < 0 else 1

        if mod == 0:
            result = 0
        else:
            result = (abs(val) % abs(mod) * pos_or_neg) #possibly add this on this line  & (2*256-1)

        return self.stack.push(signed_to_unsigned(result))


    #OPCODE     GAS
    #08         8  
    def ADDMOD(self) -> int:
        #(a:int, b:int, n:int
        #ADD TWO VALUES, THEN MODULUS
        a = self.stack.pop()
        b = self.stack.pop()
        n = self.stack.pop()

        if(n==0):
            return self.stack.push(0)
        else:
            return self.stack.push((a+b)%n)

    #OPCODE     GAS
    #09         8  
    def MULMOD(self) -> int:
        #(a:int, b:int, n:int
        #MULTIPLY TWO VALUES, THEN MODULUS
        a = self.stack.pop()
        b = self.stack.pop()
        n = self.stack.pop()

        if(n==0):
            return self.stack.push(0)
        else:
            return self.stack.push((a*b)%n)

    #OPCODE     GAS
    #0A         10   dynamic  
    def EXP(self) -> int:
        #(a:int (base), exponent:int
        #EXPONENT
        a = self.stack.pop()
        exponent = self.stack.pop()

        if(exponent ==0):
            return self.stack.push(1)
        elif(a==1):
            return self.stack.push(0)
        else:
            #TODO  ADD MODULUS? (3rd parameter in .pow) -> (2**256)
            return self.stack.push(pow(a**exponent)) 



    #OPCODE     GAS
    #0B         5  
    def SIGNEXTEND(self) -> int:
        #(b:int (bits), x:int (value)
        #Extend length of two’s complement signed integer

        #official implementation

        b = self.stack.pop()
        x = self.stack.pop()

        if b < 32:
            testbit = b * 8 + 7
            sign_bit = 1 << testbit
            if x & sign_bit:
                result = x | ((2**256) - sign_bit)
            else:
                result = x & (sign_bit - 1)
        else:
            result = x
        return self.stack.push(result)







    #Comparison & Bitwise Logic Operations


    #OPCODE     GAS
    #10         3  
    def LT(a:int, b:int) -> int:
        #LESS THAN
        return a<b

    #OPCODE     GAS
    #11         3  
    def GT(a:int, b:int) -> int:
        #GREATER THAN
        return a>b

    #OPCODE     GAS
    #12         3  
    def SLT(a:int, b:int) -> int:
        #SIGNED LESS THAN
        return a<b

    #OPCODE     GAS
    #13         3  
    def SGT(a:int, b:int) -> int:
        #SIGNED GREATER THAN
        return a>b

    #OPCODE     GAS
    #14         3  
    def EQ(a:int, b:int) -> int:
        #EQUAL
        return a==b

    #OPCODE     GAS
    #15         3  
    def ISZERO(a:int) -> int:
        return a==0

    #OPCODE     GAS
    #16         3  
    def AND(a:int, b:int) -> int:
        #BITWISE AND
        return a&b


    #OPCODE     GAS
    #17         3  
    def OR(a:int, b:int) -> int:
        #BITWISE OR
        return a|b

    #OPCODE     GAS
    #18         3  
    def XOR(a:int, b:int) -> int:
        #BITWISE XOR
        return a^b

    #OPCODE     GAS
    #19         3  
    def NOT(a:int) -> int:
        #BITWISE NOT
        return None #!a
        

    #OPCODE     GAS
    #1A         3  
    def BYTE(i:int,x:bytes) -> int:
        #offset and byte value
        #RETRIEVE SINGLE BYTE FROM WORD
        return None

    #OPCODE     GAS
    #1B         3  
    def SHL(shift:int,value:bytes) -> bytes:
        #SHIFT shift VALUE value to the LEFT
        return None

    #OPCODE     GAS
    #1C         3  
    def SHR(shift:int,value:bytes) -> bytes:
        #SHIFT shift VALUE value to the RIGHT
        return None

    #OPCODE     GAS
    #1D         3  
    def SAR(shift:int,value:bytes) -> bytes:
        #SHIFT shift VALUE value to the RIGHT
        #Shift the bits towards the least significant one. The bits moved before the first one are discarded, 
        #the new bits are set to 0 if the previous most significant bit was 0, otherwise the new bits are set to 1.
        return None




    #Comparison & Bitwise Logic Operations

    #OPCODE     GAS
    #20         30+   dynamic  
    def SHA3(offset:int,size:int) -> bytes:
        #Compute Keccak-256 hash
        return None





    #Environmental Information

    #OPCODE     GAS
    #30         2 
    def ADDRESS() -> bytes:
        #gets address of msg.sender
        return None

    #OPCODE     GAS
    #31         100 hot 3200 cold  dynamic  
    def BALANCE(address:bytes) -> int:
        #Checks the balance of given address
        return None

    #OPCODE     GAS
    #32         2  
    def ORIGIN() -> bytes:
        #Get execution origination address
        return None

    #OPCODE     GAS
    #33         2  
    def CALLER() -> bytes:
        #Get caller address
        return None

    #OPCODE     GAS
    #34         2  
    def CALLVALUE() -> int:
        #Get deposited value by the instruction/transaction responsible for this execution
        return None

    #OPCODE     GAS
    #35         3  
    def CALLDATALOAD(i:int) -> bytes:
        #byte offset i, Get input data of current environment
        return None

    #OPCODE     GAS
    #36         2  
    def CALLDATASIZE() -> int:
        #Get size of input data in current environment
        return None


    #OPCODE     GAS
    #37         3 dynamic
    def CALLDATACOPY(dest_offset:int, offset:int,size:int):
        #Copy input data in current environment to memory
        return None

    #OPCODE     GAS
    #38         2  
    def CODESIZE() -> int:
        #Get size of code running in current environment
        return None

    #OPCODE     GAS
    #39         3 dynamic
    def CODECOPY(dest_offset:int, offset:int,size:int) -> int:
        #Copy code running in current environment to memory
        return None 
        

    #OPCODE     GAS
    #3A         2  
    def GASPRICE() -> int:
        #Get price of gas in current environment
        return None

    #OPCODE     GAS
    #3B         100 dynamic  
    def EXTCODESIZE(address:bytes) -> int:
        #Get size of an account’s code
        return None

    #OPCODE     GAS
    #3C         100 dynamic  
    def EXTCODECOPY(address:bytes,dest_offset:int, offset:int,size:int):
        #Copy an account’s code to memory
        return None

    #OPCODE     GAS
    #3D         2  
    def RETURNDATASIZE() -> int:
        #Get size of output data from the previous call from the current environment
        return None

    #OPCODE     GAS
    #3E         3  dynamic
    def RETURNDATACOPY(dest_offset:int, offset:int,size:int):
        #Copy output data from the previous call to memory
        return None

    #OPCODE     GAS
    #3F         100 dynamic  
    def EXTCODEHASH(ADDRESS:bytes) -> bytes:
        #Get hash of an account’s code
        return None







    #Block Information


    #OPCODE     GAS
    #40         20 
    def BLOCKHASH(block_number:int) -> bytes:
        #Get the hash of one of the 256 most recent complete blocks
        return None

    #OPCODE     GAS
    #41         2
    def COINBASE() -> bytes:
        #Get the block’s beneficiary address
        return None

    #OPCODE     GAS
    #42         2  
    def TIMESTAMP() -> bytes:
        #Get the block’s timestamp
        return None

    #OPCODE     GAS
    #43         2  
    def NUMBER() -> int:
        #Get the block’s number
        return None

    #OPCODE     GAS
    #44         2  
    def DIFFICULTY() -> int:
        #Get the block’s difficulty
        return None

    #OPCODE     GAS
    #45         2  
    def GASLIMIT() -> bytes:
        #Get the block’s gas limit
        return None

    #OPCODE     GAS
    #46         2  
    def CHAINID() -> int:
        #Get the chain ID
        return None


    #OPCODE     GAS
    #47         5
    def SELFBALANCE() -> int:
        #Get balance of currently executing account
        return None

    #OPCODE     GAS
    #48         2  
    def BASEFEE() -> int:
        #Get the base fee
        return None







    #Stack, Memory, Storage and Flow Operations


    #OPCODE     GAS
    #50         2 
    def POP(y:bytes):
        #Remove item from stack
        return None

    #OPCODE     GAS
    #51         3 dynamic  
    def MLOAD(offset:int) -> bytes:
        #Load word from memory
        return None

    #OPCODE     GAS
    #52         3 dynamic    
    def MSTORE(offset:int,value:bytes):
        #Save word to memory
        return None

    #OPCODE     GAS
    #53         3 dynamic    
    def MSTORE8(offset:int,value:bytes):
        #Save byte to memory
        return None

    #OPCODE     GAS
    #54         100 dynamic    
    def SLOAD(key:bytes) -> int:
        #Load word from storage
        return None

    #OPCODE     GAS
    #55         100 dynamic  
    def SSTORE(key:bytes,value:bytes):
        #Save word to storage
        return None

    #OPCODE     GAS
    #56         8  
    def JUMP(counter:int):
        #Alter the program counter
        return None


    #OPCODE     GAS
    #57         10
    def JUMPI(counter:int,b:bytes):
        #Conditionally alter the program counter
        return None

    #OPCODE     GAS
    #58         2  
    def PC() -> bytes:
        #Get the value of the program counter prior to the increment corresponding to this instruction
        return None

    #OPCODE     GAS
    #59         2
    def MSIZE() -> int:
        #Get the size of active memory in bytes
        return None 
        

    #OPCODE     GAS
    #5A         2  
    def GAS() -> int:
        #Get the amount of available gas, including the corresponding reduction for the cost of this instruction
        return None

    #OPCODE     GAS
    #5B         1 
    def JUMPDEST():
        #Mark a valid destination for jumpADD
        return None


    #OPCODE     GAS
    #5F         2   
    def PUSH0() -> int:
        #Place 0 bytes item on stack
        return 0





    # Push Operations

    #OPCODE     GAS
    #60         3   
    def PUSH1(self) -> int:
        #Place 1 bytes item on stack
        self.stack.push(self.executor.processBytecode(1))
        return None

    #OPCODE     GAS
    #61         3   
    def PUSH2() -> int:
        #Place 2 bytes item on stack
        return None

    #OPCODE     GAS
    #62         3   
    def PUSH3() -> int:
        #Place 3 bytes item on stack
        return None

    #OPCODE     GAS
    #63         3   
    def PUSH4() -> int:
        #Place 4 bytes item on stack
        return None

    #OPCODE     GAS
    #64         3   
    def PUSH5() -> int:
        #Place 5 bytes item on stack
        return None

    #OPCODE     GAS
    #65         3   
    def PUSH6() -> int:
        #Place 6 bytes item on stack
        return None

    #OPCODE     GAS
    #66         3   
    def PUSH7() -> int:
        #Place 7 bytes item on stack
        return None

    #OPCODE     GAS
    #67         3   
    def PUSH8() -> int:
        #Place 8 bytes item on stack
        return None

    #OPCODE     GAS
    #68         3   
    def PUSH9() -> int:
        #Place 9 bytes item on stack
        return None

    #OPCODE     GAS
    #69         3   
    def PUSH10() -> int:
        #Place 10 bytes item on stack
        return None

    #OPCODE     GAS
    #6A         3   
    def PUSH11() -> int:
        #Place 11 bytes item on stack
        return None

    #OPCODE     GAS
    #6B         3   
    def PUSH12() -> int:
        #Place 12 bytes item on stack
        return None

    #OPCODE     GAS
    #6C         3   
    def PUSH13() -> int:
        #Place 13 bytes item on stack
        return None

    #OPCODE     GAS
    #6D         3   
    def PUSH14() -> int:
        #Place 14 bytes item on stack
        return None

    #OPCODE     GAS
    #6E         3   
    def PUSH15() -> int:
        #Place 15 bytes item on stack
        return None

    #OPCODE     GAS
    #6F         3   
    def PUSH16() -> int:
        #Place 16 bytes item on stack
        return None


    #70s

    #OPCODE     GAS
    #70         3   
    def PUSH17() -> int:
        #Place 17 bytes item on stack
        return None

    #OPCODE     GAS
    #71         3   
    def PUSH18() -> int:
        #Place 18 bytes item on stack
        return None

    #OPCODE     GAS
    #72         3   
    def PUSH19() -> int:
        #Place 19 bytes item on stack
        return None

    #OPCODE     GAS
    #73         3   
    def PUSH20() -> int:
        #Place 20 bytes item on stack
        return None

    #OPCODE     GAS
    #74         3   
    def PUSH21() -> int:
        #Place 21 bytes item on stack
        return None

    #OPCODE     GAS
    #75         3   
    def PUSH22() -> int:
        #Place 22 bytes item on stack
        return None

    #OPCODE     GAS
    #76         3   
    def PUSH23() -> int:
        #Place 23 bytes item on stack
        return None

    #OPCODE     GAS
    #77         3   
    def PUSH24() -> int:
        #Place 24 bytes item on stack
        return None

    #OPCODE     GAS
    #78         3   
    def PUSH25() -> int:
        #Place 25 bytes item on stack
        return None

    #OPCODE     GAS
    #79         3   
    def PUSH26() -> int:
        #Place 26 bytes item on stack
        return None

    #OPCODE     GAS
    #7A         3   
    def PUSH27() -> int:
        #Place 27 bytes item on stack
        return None

    #OPCODE     GAS
    #7B         3   
    def PUSH28() -> int:
        #Place 28 bytes item on stack
        return None

    #OPCODE     GAS
    #7C         3   
    def PUSH29() -> int:
        #Place 29 bytes item on stack
        return None

    #OPCODE     GAS
    #7D         3   
    def PUSH30() -> int:
        #Place 30 bytes item on stack
        return None

    #OPCODE     GAS
    #7E         3   
    def PUSH31() -> int:
        #Place 31 bytes item on stack
        return None

    #OPCODE     GAS
    #7F         3   
    def PUSH32() -> int:
        #Place 32 bytes item on stack
        return None






    #Duplication Operations


    #OPCODE     GAS
    #80         3   
    def DUP1(value:bytes) -> bytes:
        #Duplicate 1st stack item
        return None

    #OPCODE     GAS
    #81         3   
    def DUP2(value:bytes) -> bytes:
        #Duplicate 2nd stack item
        return None

    #OPCODE     GAS
    #82         3   
    def DUP3(value:bytes) -> bytes:
        #Duplicate 3rd stack item
        return None

    #OPCODE     GAS
    #83         3   
    def DUP4(value:bytes) -> bytes:
        #Duplicate 4th stack item
        return None

    #OPCODE     GAS
    #84         3   
    def DUP5(value:bytes) -> bytes:
        #Duplicate 5th stack item
        return None

    #OPCODE     GAS
    #85         3   
    def DUP6(value:bytes) -> bytes:
        #Duplicate 6th stack item
        return None

    #OPCODE     GAS
    #86         3   
    def DUP7(value:bytes) -> bytes:
        #Duplicate 7th stack item
        return None

    #OPCODE     GAS
    #87         3   
    def DUP8(value:bytes) -> bytes:
        #Duplicate 8th stack item
        return None

    #OPCODE     GAS
    #88         3   
    def DUP9(value:bytes) -> bytes:
        #Duplicate 9th stack item
        return None

    #OPCODE     GAS
    #89         3   
    def DUP10(value:bytes) -> bytes:
        #Duplicate 10th stack item
        return None

    #OPCODE     GAS
    #8A         3   
    def DUP11(value:bytes) -> bytes:
        #Duplicate 11th stack item
        return None

    #OPCODE     GAS
    #8B         3   
    def DUP12(value:bytes) -> bytes:
        #Duplicate 12th stack item
        return None

    #OPCODE     GAS
    #8C         3   
    def DUP13(value:bytes) -> bytes:
        #Duplicate 13th stack item
        return None

    #OPCODE     GAS
    #8D         3   
    def DUP14(value:bytes) -> bytes:
        #Duplicate 14th stack item
        return None

    #OPCODE     GAS
    #8E         3   
    def DUP15(value:bytes) -> bytes:
        #Duplicate 15th stack item
        return None

    #OPCODE     GAS
    #8F         3   
    def DUP16(value:bytes) -> bytes:
        #Duplicate 16th stack item
        return None









    #Exchange Operations


    #OPCODE     GAS
    #90         3   
    def SWAP1(a:bytes,b:bytes) -> bytes:
        #Exchange 1st and 2nd stack items
        return None

    #OPCODE     GAS
    #91         3   
    def SWAP2(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 3rd stack items 
        return None

    #OPCODE     GAS
    #92         3   
    def SWAP3(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 4th stack items
        return None

    #OPCODE     GAS
    #93         3   
    def SWAP4(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 5th stack items
        return None

    #OPCODE     GAS
    #94         3   
    def SWAP5(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 6th stack items
        return None

    #OPCODE     GAS
    #95         3   
    def SWAP6(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 7th stack items
        return None

    #OPCODE     GAS
    #96         3   
    def SWAP7(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 8th stack items
        return None

    #OPCODE     GAS
    #97         3   
    def SWAP8(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 9th stack items
        return None

    #OPCODE     GAS
    #98         3   
    def SWAP9(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 10th stack items
        return None

    #OPCODE     GAS
    #99         3   
    def SWAP10(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 11th stack items
        return None

    #OPCODE     GAS
    #9A         3   
    def SWAP11(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 12th stack items
        return None

    #OPCODE     GAS
    #9B         3   
    def SWAP12(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 13th stack items
        return None

    #OPCODE     GAS
    #9C         3   
    def SWAP13(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 14th stack items
        return None

    #OPCODE     GAS
    #9D         3   
    def SWAP14(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 15th stack items
        return None

    #OPCODE     GAS
    #9E         3   
    def SWAP15(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 16th stack items
        return None

    #OPCODE     GAS
    #9F         3   
    def SWAP16(a:bytes,ignored:bytes,b:bytes) -> bytes:# ignored return types in the middle DO LATER
        #Exchange 1st and 17th stack items
        return None






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
    def REVERT(dest_offset:int, offset:int,size:int):
        #Halt execution reverting state changes but returning data and remaining gas
        return None

    #OPCODE     GAS
    #FE         NaN dynamic  
    def INVALID() -> int:
        #Designated invalid instruction
        return None

    #OPCODE     GAS
    #FF         5000 dynamic   
    def SELFDESTRUCT(address:bytes):
        #Halt execution and register account for later deletion
        return None 
        