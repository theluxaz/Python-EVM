from executor import Executor
from opcode_list import opcodes_list
from execution_context import ExecutionContext


hexcode = "4142434445464748"

starting_gas = 40000
execution_context_data = {"block_hash": 0xbc0ecefe7626a1fba4a136446afe38dd516e881a770743045d468a4bf098a2b3, 
                 "block_number":17534772,
                 "block_difficulty":58750003716598352816469,
                 "coinbase": 0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5, 
                 "timestamp": 1687432199,
                 "gas_limit":30000000,
                 "chain_id":1, 
                 "base_fee":29658770000,
                 "self_balance":1000000000000000000
                 }


def main(bytecode: bytearray ) -> None:
    #Runs code

    execution_context = ExecutionContext(*execution_context_data.values())
    executor = Executor(bytecode=bytecode,execution_context=execution_context,opcodes_list= opcodes_list,starting_gas=starting_gas)
    executor.run()


if __name__ == "__main__":
    main(bytearray.fromhex(hexcode))