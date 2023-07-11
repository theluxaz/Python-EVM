from executor import Executor
from opcode_list import opcodes_list
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from external_contract import ExternalContract


hexcode = "608060405234801561001057600080fd5b50610150806100206000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c80632e64cec11461003b5780636057361d14610059575b600080fd5b610043610075565b60405161005091906100a1565b60405180910390f35b610073600480360381019061006e91906100ed565b61007e565b005b60008054905090565b8060008190555050565b6000819050919050565b61009b81610088565b82525050565b60006020820190506100b66000830184610092565b92915050565b600080fd5b6100ca81610088565b81146100d557600080fd5b50565b6000813590506100e7816100c1565b92915050565b600060208284031215610103576101026100bc565b5b6000610111848285016100d8565b9150509291505056fea2646970667358221220322c78243e61b783558509c9cc22cb8493dde6925aa5e89a08cdf6e22f279ef164736f6c63430008120033"

                 #TODO TO change below bytearray.fromhex()??
external_contracts ={
                0x95222290DD7278Aa3Ddd389Cc1E1d165C04BA000:{"bytecode":"604260005260206000F3","balance":1000000000000000000},         
                0x95222290DD7278Aa3Ddd389Cc1E1d165C04BA021:{"bytecode":"60426000526020600060046000600038","balance":2000000000000000000}
                }

# starting_gas = 40000
execution_context_data = {"block_hash": 0xbc0ecefe7626a1fba4a136446afe38dd516e881a770743045d468a4bf098a2b3, 
                 "block_number":17534772,
                 "block_difficulty":58750003716598352816469,
                 "coinbase": 0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5, 
                 "timestamp": 1687432199,
                 "gas_limit":30000000,
                 "chain_id":1, 
                 "base_fee":29658770000,
                 "self_balance":1000000000000000000,
                 "self_address":0x95222290DD7278Aa3Ddd389Cc1E1d165C0000000,
                 "external_contracts":external_contracts
                 }

transaction_context_data = {"sender_address": 0x95222290DD7278Aa3Ddd389Cc1E1d165C04BAfe1, 
                 "origin_address": 0x95222290DD7278Aa3Ddd389Cc1E1d165C04BAfe1, 
                 "value":100000000000000000,
                 #TODO TO change below to bytearray.fromhex()??
                 "data": 0x05030201, #
                 "gas_price": 29658773020,
                 "gas": 40000,
                 "nonce": 4
                 }



def run(bytecode: bytearray, execution_context_data:dict,transaction_context_data:dict):
    #Runs code
    execution_context = ExecutionContext(*execution_context_data.values())
    transaction_context = TransactionContext(*transaction_context_data.values())
    executor = Executor(bytecode=bytecode,execution_context=execution_context,transaction_context=transaction_context)
    
    result = executor.run()
    executor.print_logs()
    
    return result

def main() -> None:
    #Runs code
    bytecode = bytearray.fromhex(hexcode)
    result = run(bytecode,execution_context_data,transaction_context_data)

    print("FINISHED EXECUTION")
    print(result)
    


if __name__ == "__main__":
    main()

def process_external_contracts(external_contracts:dict):
    external_contracts_list =[]
    for key,value in external_contracts.items():
            external_contracts_list.append(ExternalContract(key.to_bytes(20, byteorder = 'big'), bytearray.fromhex(value)))

    return external_contracts_list