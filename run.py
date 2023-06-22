from executor import Executor
from opcode_list import opcodes_list
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from external_contract import ExternalContract


hexcode = "602060006004600060007395222290dd7278aa3ddd389cc1e1d165c04ba0213c"

                 #TODO TO change below bytearray.fromhex()??
external_contracts ={
                0x95222290DD7278Aa3Ddd389Cc1E1d165C04BA000:"604260005260206000F3",         
                0x95222290DD7278Aa3Ddd389Cc1E1d165C04BA021:"60426000526020600060046000600038"
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
                 "external_contracts":external_contracts
                 }

transaction_context_data = {"sender_address": 0x95222290DD7278Aa3Ddd389Cc1E1d165C04BAfe1, 
                 "origin_address": 0x95222290DD7278Aa3Ddd389Cc1E1d165C04BAfe1, 
                 "value":100000000000000000,
                 #TODO TO change below to bytearray.fromhex()??
                 "data": 0x05030201, #
                 "gas_price": 29658773020,
                 "gas": 40000
                 }




def main(bytecode: bytearray ) -> None:
    #Runs code

    # execution_context_data[external_contracts] = process_external_contracts(external_contracts)
    execution_context = ExecutionContext(*execution_context_data.values())
    transaction_context = TransactionContext(*transaction_context_data.values())
    executor = Executor(bytecode=bytecode,execution_context=execution_context,transaction_context=transaction_context)
    executor.run()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))

def process_external_contracts(external_contracts:dict):
    external_contracts_list =[]
    for key,value in external_contracts.items():
            external_contracts_list.append(ExternalContract(key.to_bytes(20, byteorder = 'big'), bytearray.fromhex(value)))

    return external_contracts_list