from execution_context import ExecutionContext
from transaction_context import TransactionContext
from executor import Executor

class ContractInstance:

    def __init__(self,execution_context:ExecutionContext,transaction_context:TransactionContext) -> None:
        self.execution_context=execution_context
        self.transaction_context=transaction_context
    
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
        if(result and result != "REVERT" and result != "INVALID"):
            print("doping true")
            if(list(executor.instructions.stack.stack)):
                return (True, list(reversed((list(executor.instructions.stack.stack)))))
            else:
                return (True, list(executor.instructions.stack.stack))
        else:
            if(list(executor.instructions.stack.stack)):
                return (False, list(reversed((list(executor.instructions.stack.stack)))))
            else:
                return (False, list(executor.instructions.stack.stack))
    
    def static_call(self,gas,address,calldata):
        #Runs code
        print("Running STATIC CALL --------------------------------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        external_bytecode = bytearray.fromhex(self.execution_context.external_contracts[address]["bytecode"])
        
        transaction_context_static =  TransactionContext(self.execution_context.self_address,self.transaction_context.origin_address,0,calldata,self.transaction_context.gas_price,gas,self.transaction_context.nonce+1)
                                                         
        # transaction_context_static["sender_address"] = self.execution_context["self_address"]
        # transaction_context_static["data"] = calldata
        # transaction_context_static["gas"] = gas      
        
        executor = Executor(self,bytecode=external_bytecode,execution_context=self.execution_context,transaction_context=transaction_context_static)
        result = executor.run()
        executor.print_logs()
        return result
