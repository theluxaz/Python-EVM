import json
import os
from opcode_list import opcodes_list
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from external_contract import ExternalContract
from contract_instance import ContractInstance
# from contract_handler import ContractHandler

#created storage contract 
#608060405234801561001057600080fd5b50600760008190555060b6806100276000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80632e64cec114602d575b600080fd5b60336047565b604051603e91906067565b60405180910390f35b60008054905090565b6000819050919050565b6061816050565b82525050565b6000602082019050607a6000830184605a565b9291505056fea26469706673582212209f86e49e78e1f27c3f63d1e1f0b394957740f7e0efef5bbcbc42937c9a7a85c564736f6c63430008120033

#RAW of above with initialization
#608060405234801561001057600080fd5b50600760008190555060b6806100276000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80632e64cec114602d575b600080fd5b60336047565b604051603e91906067565b60405180910390f35b60008054905090565b6000819050919050565b6061816050565b82525050565b6000602082019050607a6000830184605a565b9291505056fea26469706673582212209f86e49e78e1f27c3f63d1e1f0b394957740f7e0efef5bbcbc42937c9a7a85c564736f6c63430008120033

# hexcode = "60016000600060007395222290dd7278aa3ddd389cc1e1d165c04b1111622dc6c0fa"
#test callvalue

hexcode = "60606040523415600e57600080fd5b5b603680601c6000396000f300"

TESTING =True

#DATA
external_contracts ={
                "95222290DD7278Aa3Ddd389Cc1E1d165C04BA000":{"bytecode":"604260005260206000F3","balance":1000000000000000000},         
                "95222290DD7278Aa3Ddd389Cc1E1d165C04BA021":{"bytecode":"60426000526020600060046000600038","balance":2000000000000000000},
                "1e79b045dc29eae9fdc69673c9dcd7c53e5e159d":{"bytecode":"","balance":256},#test case
                "1000000000000000000000000000000000000aaa":{"bytecode":"6001","balance":9},#test case
                "1000000000000000000000000000000000000aab":{"bytecode":"FFFFFFFF","balance":0},#test case
                "1000000000000000000000000000000000000c42":{"bytecode":"60426000526001601ff3","balance":0},#test case CALL 1
                "1000000000000000000000000000000000000c43":{"bytecode":"3360005260206000f3","balance":0},#test case CALL 2
                "1000000000000000000000000000000000000c44":{"bytecode":"60426000526001601ffd","balance":0},#test case CALL 3
                "dddddddddddddddddddddddddddddddddddddddd":{"bytecode":"30600055","balance":0},#test case DELEGATE CALL 1
                "1000000000000000000000000000000000000c4d":{"bytecode":"30600055","balance":0},#test case STATIC CALL 2
                "dead00000000000000000000000000000000dead":{"bytecode":"731000000000000000000000000000000000000aaaff","balance":7},#test case SELF DESTRUCT 1
                "95222290DD7278Aa3Ddd389Cc1E1d165C04B1111":{"bytecode":"608060405234801561001057600080fd5b50600760008190555060b6806100276000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80632e64cec114602d575b600080fd5b60336047565b604051603e91906067565b60405180910390f35b60008054905090565b6000819050919050565b6061816050565b82525050565b6000602082019050607a6000830184605a565b9291505056fea26469706673582212209f86e49e78e1f27c3f63d1e1f0b394957740f7e0efef5bbcbc42937c9a7a85c564736f6c63430008120033","balance":2000000000000000000}
                }

execution_context_data = {"block_hash": "bc0ecefe7626a1fba4a136446afe38dd516e881a770743045d468a4bf098a2b3", 
                 "block_number":16777217,
                 "block_prevrandao":131072,
                 "coinbase": "95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5", 
                 "timestamp": 15000001,
                 "gas_limit":281474976710655,
                 "chain_id":1, 
                 "base_fee":1,
                 "self_balance":512,
                 "external_contracts":external_contracts
                 }

transaction_context_data = {"caller_address": "1e79b045dc29eae9fdc69673c9dcd7c53e5e159d", 
                            "to_address":"1000000000000000000000000000000000000aaa",
                 "origin_address": "1000000000000000000000000000000000001337", 
                 "value":4096, 
                 "data": "000102030405060708090a0b0c0d0e0f00112233445566778899aabbccddeeff", #CALLDATA
                 "gas_price": 153,
                 "gas": 4000000000,
                 "nonce": 4
                 }


def start(bytecode: bytearray, execution_context_data:dict,transaction_context_data:dict):
    contract_instance_main = ContractInstance(ExecutionContext(*execution_context_data.values()),TransactionContext(*transaction_context_data.values()))
    result = contract_instance_main.run_instance(bytecode)
    return result

def main() -> None:
    #Runs code
    bytecode = bytearray.fromhex(hexcode)
    result = start(bytecode,execution_context_data,transaction_context_data)

    print("FINISHED EXECUTION")
    print(result)
    print()
    if(type(result) == int):
        print(f"FINAL result is : int {result}")
    else:
        print(f"FINAL result is : bytes {result.hex()}")
       
       
def start_testing(bytecode: bytearray, execution_context_data:dict,transaction_context_data:dict):
    contract_instance_main = ContractInstance(ExecutionContext(*execution_context_data.values()),TransactionContext(*transaction_context_data.values()))
    return contract_instance_main.run_instance_test(bytecode)

        
def main_testing(code) -> None:
    #Runs code
    return start_testing(code,execution_context_data,transaction_context_data)
    


def test():
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dirname,"evm.json")
    with open(json_file) as f:
        data = json.load(f)
        total = len(data)

        for i, test in enumerate(data):
            print()
            print(f"💠 Starting Test #{i + 1}/{total} {test['name']}")
            print()
            # Note: as the test cases get more complex, you'll need to modify this
            # to pass down more arguments to the evm function
            # print(f"i is {i}  ,  test is {test} ===============")
            code = bytearray.fromhex(test['code']['bin'])
            # print(f"Code is {str(code)} ----------------------------- ===============")
            (success,stack,logs) = main_testing(code)

            # expected_stack = [int(x, 16) for x in test['expect']['stack']]
            expected_stack = None
            expected_logs = None
            if(test["expect"].get('logs')):
                expected_logs = [x for x in test['expect']['logs']]
                if logs != expected_logs or success != test['expect']['success']:
                    print()
                    print(f"❌ Test #{i + 1}/{total} {test['name']}")
                    print()
                    if logs != expected_logs:
                        print("Stack doesn't match")
                        print(" expected:", expected_logs)
                        print("   actual:", logs)
                    else:
                        print("Success doesn't match")
                        print(" expected:", test['expect']['success'])
                        print("   actual:", success)
                    print("")
                    print("Test code:")
                    print(test['code']['asm'])
                    print("")
                    print("Hint:", test['hint'])
                    print("")
                    print(f"Progress: {i}/{len(data)}")
                    print("")
                    break
                else:
                    print()
                    print(f"✅ Test #{i + 1}/{total} {test['name']}")
                    print()


            if(test["expect"].get('stack')):
                expected_stack = [bytearray(int(x, 16).to_bytes((int(x, 16).bit_length() + 7) // 8, byteorder = 'big')) for x in test['expect']['stack']]
                if stack != expected_stack or success != test['expect']['success']:
                    print()
                    print(f"❌ Test #{i + 1}/{total} {test['name']}")
                    print()
                    if stack != expected_stack:
                        print("Stack doesn't match")
                        print(" expected:", expected_stack)
                        print("   actual:", stack)
                    else:
                        print("Success doesn't match")
                        print(" expected:", test['expect']['success'])
                        print("   actual:", success)
                    print("")
                    print("Test code:")
                    print(test['code']['asm'])
                    print("")
                    print("Hint:", test['hint'])
                    print("")
                    print(f"Progress: {i}/{len(data)}")
                    print("")
                    break
                else:
                    print()
                    print(f"✅ Test #{i + 1}/{total} {test['name']}")
                    print()
                
                



if __name__ == "__main__":
    if(TESTING):
        test()
    else:
        main()
    

def process_external_contracts(external_contracts:dict):
    external_contracts_list =[]
    for key,value in external_contracts.items():
            external_contracts_list.append(ExternalContract(key.to_bytes(20, byteorder = 'big'), bytearray.fromhex(value)))

    return external_contracts_list
