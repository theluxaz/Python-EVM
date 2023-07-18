import json
import os
from opcode_list import opcodes_list
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from contract_instance import ContractInstance
from state import State


hexcode = "6006600455600654"

TESTING = True

execution_context_data = {
    "block_hash": "bc0ecefe7626a1fba4a136446afe38dd516e881a770743045d468a4bf098a2b3",
    "block_number": 16777217,
    "block_prevrandao": 131072,
    "coinbase": "95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5",
    "timestamp": 15000001,
    "gas_limit": 281474976710655,
    "chain_id": 1,
    "base_fee": 1,
}

transaction_context_data = {
    "caller_address": "1e79b045dc29eae9fdc69673c9dcd7c53e5e159d",
    "to_address": "1000000000000000000000000000000000000aaa",
    "origin_address": "1000000000000000000000000000000000001337",
    "value": 4096,
    "data": "000102030405060708090a0b0c0d0e0f00112233445566778899aabbccddeeff",  # CALLDATA
    "gas_price": 153,
    "gas": 4000000000,
    "nonce": 4,
}


# TODO This file needs heavy refactoring


def main() -> None:
    # Runs code
    bytecode = bytearray.fromhex(hexcode)
    contract_instance_main = ContractInstance(
        ExecutionContext(*execution_context_data.values()),
        TransactionContext(*transaction_context_data.values()),
        State(False),
        TESTING,
    )
    result = contract_instance_main.run_instance(bytecode)

    print("FINISHED EXECUTION")
    print()
    if type(result) == int:
        print(f"FINAL result is : int {result}")
    else:
        print(f"FINAL result is :  {result}")


def main_testing(code) -> None:
    # Runs code
    contract_instance_main = ContractInstance(
        ExecutionContext(*execution_context_data.values()),
        TransactionContext(*transaction_context_data.values()),
        State(True),
        TESTING,
    )
    return contract_instance_main.run_instance_test(code)


def test():
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dirname, "evm.json")
    with open(json_file) as f:
        data = json.load(f)
        total = len(data)

        for i, test in enumerate(data):
            print()
            print(f"💠 Starting Test #{i + 1}/{total} {test['name']}")
            print()
            # Note: as the test cases get more complex, you'll need to modify this
            # to pass down more arguments to the evm function
            code = bytearray.fromhex(test["code"]["bin"])
            (success, stack, logs) = main_testing(code)

            expected_stack = None
            expected_logs = None
            if test["expect"].get("logs"):
                expected_logs = [x for x in test["expect"]["logs"]]
                if logs != expected_logs or success != test["expect"]["success"]:
                    print()
                    print(f"❌ Test #{i + 1}/{total} {test['name']}")
                    print()
                    if logs != expected_logs:
                        print("Stack doesn't match")
                        print(" expected:", expected_logs)
                        print("   actual:", logs)
                    else:
                        print("Success doesn't match")
                        print(" expected:", test["expect"]["success"])
                        print("   actual:", success)
                    print("")
                    print("Test code:")
                    print(test["code"]["asm"])
                    print("")
                    print("Hint:", test["hint"])
                    print("")
                    print(f"Progress: {i}/{len(data)}")
                    print("")
                    break
                else:
                    print()
                    print(f"✅ Test #{i + 1}/{total} {test['name']}")
                    print()

            if test["expect"].get("stack"):
                expected_stack = [
                    bytearray(
                        int(x, 16).to_bytes(
                            (int(x, 16).bit_length() + 7) // 8, byteorder="big"
                        )
                    )
                    for x in test["expect"]["stack"]
                ]
                if stack != expected_stack or success != test["expect"]["success"]:
                    print()
                    print(f"❌ Test #{i + 1}/{total} {test['name']}")
                    print()
                    if stack != expected_stack:
                        print("Stack doesn't match")
                        print(" expected:", expected_stack)
                        print("   actual:", stack)
                    else:
                        print("Success doesn't match")
                        print(" expected:", test["expect"]["success"])
                        print("   actual:", success)
                    print("")
                    print("Test code:")
                    print(test["code"]["asm"])
                    print("")
                    print("Hint:", test["hint"])
                    print("")
                    print(f"Progress: {i}/{len(data)}")
                    print("")
                    break
                else:
                    print()
                    print(f"✅ Test #{i + 1}/{total} {test['name']}")
                    print()


if __name__ == "__main__":
    if TESTING:
        test()
    else:
        main()
