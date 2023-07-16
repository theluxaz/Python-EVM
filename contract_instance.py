from execution_context import ExecutionContext
from transaction_context import TransactionContext
from executor import Executor

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
    
    def static_call(self,gas,address,calldata):
        #Runs code
        print("STARTING STATIC CALL SUBCONTEXT --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
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
        external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
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
        external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
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
        external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
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
