from execution_context import ExecutionContext
from transaction_context import TransactionContext
from executor import Executor
from eth_hash.auto import keccak
import rlp

class ContractInstance:

    def __init__(self,execution_context:ExecutionContext,transaction_context:TransactionContext) -> None:
        self.execution_context=execution_context
        self.transaction_context=transaction_context
        self.return_data = None
    
    def run_instance(self,bytecode):
        #Runs code
        print("Running Instance --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        executor = Executor(self,bytecode=bytecode,execution_context=self.execution_context,transaction_context=self.transaction_context)
        result = executor.run()
        executor.print_logs()
        return result
    
    def run_instance_test(self,bytecode):
        #Runs code
        print("Running Instance --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        executor = Executor(self,bytecode=bytecode,execution_context=self.execution_context,transaction_context=self.transaction_context)
        result = executor.run_testing()
        executor.print_logs()
        print(result)
        if( executor.reverted == False and executor.invalid == False):
            if(list(executor.instructions.stack.stack)):
                return (True, list(reversed((list(executor.instructions.stack.stack)))), executor.logs)
            else:
                return (True, list(executor.instructions.stack.stack), executor.logs)
        else:
            if(list(executor.instructions.stack.stack)):
                return (False, list(reversed((list(executor.instructions.stack.stack)))), executor.logs)
            else:
                return (False, list(executor.instructions.stack.stack), executor.logs)
    
    def create(self,value,bytecode_data):
        #Runs code
        print()
        print("STARTING CREATE SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"External bytecode: {bytecode_data.hex()}")
        
        new_address = keccak(rlp.encode([self.transaction_context.to_address, self.transaction_context.nonce+1]))[12:]
        print(f"New address is: {new_address.hex()}")
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,new_address,self.transaction_context.origin_address,value,"",self.transaction_context.gas_price,self.transaction_context.gas,self.transaction_context.nonce+1)
        
        executor = Executor(self,bytecode=bytecode_data,execution_context=self.execution_context,transaction_context=transaction_context_call)
        result = executor.run()
        print(f"Adding return DATA : {result} -----------------------------")
        self.return_data = result
        executor.print_logs()
        # print(f"external code data 0 is {self.execution_context.external_contracts.items()}")
        # print(f"external code LEN 0 is {len(self.execution_context.external_contracts.items())}")
        
        print("ENDING CREATE SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted or executor.invalid):
            return False,False
        elif(executor.finished):
            if(result):
                self.execution_context.external_contracts[int.from_bytes(new_address, byteorder="big")] = {"balance":value,"bytecode":result.hex()}
            else:
                self.execution_context.external_contracts[int.from_bytes(new_address, byteorder="big")] = {"balance":value,"bytecode":""}
            return new_address,True
        else:
            self.execution_context.external_contracts[int.from_bytes(new_address, byteorder="big")] = {"balance":value,"bytecode":result.hex()}
            
            print(f"external code data 1 is {self.execution_context.external_contracts.items()}")
            return new_address,True
    
    def create2(self,value,bytecode_data,salt):
        #Runs code
        print()
        print("STARTING CREATE2 SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"External bytecode: {bytecode_data.hex()}")
        
        new_address = keccak(rlp.encode([b'\xff' + self.transaction_context.to_address, salt, self.transaction_context.nonce+1]))[12:]
        print(f"New address is: {new_address.hex()}")
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,new_address,self.transaction_context.origin_address,value,"",self.transaction_context.gas_price,self.transaction_context.gas,self.transaction_context.nonce+1)
        
        executor = Executor(self,bytecode=bytecode_data,execution_context=self.execution_context,transaction_context=transaction_context_call)
        result = executor.run()
        print(f"Adding return DATA : {result.hex()} -----------------------------")
        self.return_data = result
        executor.print_logs()
        # print(f"external code data 0 is {self.execution_context.external_contracts.items()}")
        # print(f"external code LEN 0 is {len(self.execution_context.external_contracts.items())}")
        
        print("ENDING CREATE2 SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted or executor.invalid):
            return False,False
        elif(executor.finished):
            if(result):
                self.execution_context.external_contracts[int.from_bytes(new_address, byteorder="big")] = {"balance":value,"bytecode":result.hex()}
            else:
                self.execution_context.external_contracts[int.from_bytes(new_address, byteorder="big")] = {"balance":value,"bytecode":""}
            return new_address,True
        else:
            self.execution_context.external_contracts[int.from_bytes(new_address, byteorder="big")] = {"balance":value,"bytecode":result.hex()}
            
            print(f"external code data 1 is {self.execution_context.external_contracts.items()}")
            return new_address,True
    
    def static_call(self,gas,address,calldata):
        #Runs code
        print("STARTING STATIC CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
        except:
            print("Address not found")
            return False,False
        print(f"External bytecode: {external_bytecode}")
        
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,address,self.transaction_context.origin_address,0,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,static=True)
        result = executor.run()
        print(f"Adding return DATA : {result} -----------------------------")
        self.return_data = result
        executor.print_logs()
        
        print("ENDING STATIC CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(executor.stopped)
        if(executor.reverted):
            return result,False
        elif(executor.invalid):
            return False,False
        else:
            return result,True
    
    def call(self,gas,address,value,calldata):
        #Runs code
        print("STARTING CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
        except:
            print("Address not found")
            return False,False
            
        print(f"External bytecode: {external_bytecode}")
        
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,address,self.transaction_context.origin_address,value,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call)
        result = executor.run()
        print(f"Adding return DATA : {result} -----------------------------")
        self.return_data = result
        executor.print_logs()
        
        print("ENDING CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted):
            return result,False
        elif(executor.invalid):
            return False,False
        else:
            return result,True
        
    def delegate_call(self,gas,address,calldata,storage):
        #Runs delegate call code
        print("STARTING DELEGATE CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
        except:
            print("Address not found")
            return False,False
            
        print(f"External bytecode: {external_bytecode}")
        
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,self.transaction_context.to_address,self.transaction_context.origin_address,self.transaction_context.value,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,storage=storage)
        result = executor.run()
        print(f"Adding return DATA : {result} -----------------------------")
        self.return_data = result
        executor.print_logs()
        
        print("ENDING DELEGATE CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted):
            return result,False
        elif(executor.invalid):
            return False,False
        else:
            return result,True
        
    #same as delegate but with value and not the same current sender??
    def call_code(self,gas,address,value,calldata,storage):
        #Runs delegate call code
        print("STARTING CALLCODE SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
        except:
            print("Address not found")
            return False,False
        print(f"External bytecode: {external_bytecode}")
        
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,self.transaction_context.to_address,self.transaction_context.origin_address,value,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,storage=storage)
        result = executor.run()
        print(f"Adding return DATA : {result} -----------------------------")
        self.return_data = result
        executor.print_logs()
        
        print("ENDING CALLCODE SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted):
            return result,False
        elif(executor.invalid):
            return False,False
        else:
            return result,True
        
    def get_return_data(self):
        return self.return_data
