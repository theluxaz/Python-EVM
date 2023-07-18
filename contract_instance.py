from execution_context import ExecutionContext
from transaction_context import TransactionContext
from executor import Executor
from state import State
from eth_hash.auto import keccak
import rlp
import json

class ContractInstance:

    def __init__(self,execution_context:ExecutionContext,transaction_context:TransactionContext,state:State) -> None:
        self.execution_context=execution_context
        self.transaction_context=transaction_context
        self.EVM_STATE = state
        self.return_data = None
    
    def run_instance(self,bytecode):
        #Runs code
        print("Running Instance!")
        executor = None
        result = None
        # try:
        executor = Executor(self,bytecode=bytecode,execution_context=self.execution_context,transaction_context=self.transaction_context,EVM_STATE=self.EVM_STATE)
        result = executor.run()
        # except Exception as error:
        #     print(error)
        #     executor.revert_transaction()
        executor.finish_transaction()
        executor.print_logs()
        self.EVM_STATE.save()
        return result
    
    def run_instance_test(self,bytecode):
        #Runs code
        print("Running Instance!")
        executor = None
        result = None
        # try:
        executor = Executor(self,bytecode=bytecode,execution_context=self.execution_context,transaction_context=self.transaction_context,EVM_STATE=self.EVM_STATE)
        result = executor.run()
        # except Exception as error:
        #     print(error)
        #     executor.revert_transaction()
        executor.finish_transaction()
        executor.print_logs()
        if( executor and executor.reverted == False and executor.invalid == False):
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
        new_address = keccak(rlp.encode([self.transaction_context.to_address, self.transaction_context.nonce+1]))[12:]
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,new_address,self.transaction_context.origin_address,value,"",self.transaction_context.gas_price,self.transaction_context.gas,self.transaction_context.nonce+1)
        
        executor = None
        result = None
        # try:
        executor = Executor(self,bytecode=bytecode_data,execution_context=self.execution_context,transaction_context=transaction_context_call,EVM_STATE=self.EVM_STATE)
        result = executor.run()
        # except Exception as error:
        #     print(error)
        #     executor.revert_transaction()
        executor.consume_gas()
        executor.update_nonce()
        
        print(f"Adding return DATA : {result} -----------------------------")
        self.return_data = result
        executor.print_logs()
        print("ENDING CREATE SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted or executor.invalid):
            return False,False
        elif(executor.finished):
            if(result):
                self.EVM_STATE.set(new_address.hex(),{"balance":value,"bytecode":result.hex(),"state":executor.instructions.storage.storage})
            else:
                self.EVM_STATE.set(new_address.hex(),{"balance":value,"bytecode":"","state":executor.instructions.storage.storage})
            return new_address,True
        else:
            self.EVM_STATE.set(new_address.hex(),{"balance":value,"bytecode":result.hex(),"state":executor.instructions.storage.storage})
            return new_address,True
    
    def create2(self,value,bytecode_data,salt):
        #Runs code
        print()
        print("STARTING CREATE2 SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        new_address = keccak(rlp.encode([b'\xff' + self.transaction_context.to_address, salt, self.transaction_context.nonce+1]))[12:]
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,new_address,self.transaction_context.origin_address,value,"",self.transaction_context.gas_price,self.transaction_context.gas,self.transaction_context.nonce+1)
        
        executor = None
        result = None
        try:
            executor = Executor(self,bytecode=bytecode_data,execution_context=self.execution_context,transaction_context=transaction_context_call,EVM_STATE=self.EVM_STATE)
            result = executor.run()
        except Exception as error:
            print(error)
            executor.revert_transaction()
        executor.consume_gas()
        executor.update_nonce()
        self.return_data = result
        executor.print_logs()
        
        print("ENDING CREATE2 SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if(executor.reverted or executor.invalid):
            return False,False
        elif(executor.finished):
            if(result):
                self.EVM_STATE.set(new_address.hex(),{"balance":value,"bytecode":result.hex(),"state":executor.instructions.storage.storage})
            else:
                self.EVM_STATE.set(new_address.hex(),{"balance":value,"bytecode":"","state":executor.instructions.storage.storage})
            return new_address,True
        else:
            self.EVM_STATE.set(new_address.hex(),{"balance":value,"bytecode":"","state":executor.instructions.storage.storage})
            return new_address,True
    
    def static_call(self,gas,address,calldata):
        #Runs code
        print("STARTING STATIC CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            external_bytecode = bytearray.fromhex(self.EVM_STATE.get(address)["bytecode"])
        except:
            print("Address not found")
            return False,False
        
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,address,self.transaction_context.origin_address,0,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = None
        result = None
        try:
            executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,static=True,EVM_STATE=self.EVM_STATE)
            result = executor.run()
        except Exception as error:
            print(error)
            executor.revert_transaction()
        executor.update_nonce()
        
        self.return_data = result
        executor.print_logs()
        
        print("ENDING STATIC CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
            external_bytecode = bytearray.fromhex(self.EVM_STATE.get(address)["bytecode"])
        except:
            print("Address not found")
            return False,False
                    
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,address,self.transaction_context.origin_address,value,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = None
        result = None
        try:
            executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,EVM_STATE=self.EVM_STATE)
            result = executor.run()
        except Exception as error:
            print(error)
            executor.revert_transaction()
        executor.finish_transaction()

        executor.update_nonce()
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
            external_bytecode = bytearray.fromhex(self.EVM_STATE.get(address)["bytecode"])
        except:
            print("Address not found")
            return False,False
                    
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,self.transaction_context.to_address,self.transaction_context.origin_address,self.transaction_context.value,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = None
        result = None
        try:
            executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,EVM_STATE=self.EVM_STATE)
            result = executor.run()
        except Exception as error:
            print(error)
            executor.revert_transaction()
        executor.finish_transaction()
        executor.update_nonce()
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
            external_bytecode = bytearray.fromhex(self.EVM_STATE.get(address)["bytecode"])
        except:
            print("Address not found")
            return False,False
        
        transaction_context_call =  TransactionContext(self.transaction_context.to_address,self.transaction_context.to_address,self.transaction_context.origin_address,value,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
        
        executor = None
        result = None
        try:
            executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_call,EVM_STATE=self.EVM_STATE)
            result = executor.run()
        except Exception as error:
            print(error)
            executor.revert_transaction()
        executor.finish_transaction()
        executor.update_nonce()
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
    
    def update_state(self,execution_context):
        self.execution_context = execution_context
