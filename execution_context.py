from external_contract import ExternalContract



class ExecutionContext:

    def __init__(self, block_hash: bytearray, 
                 block_number:int,
                 block_difficulty:int,
                 coinbase: bytearray, 
                 timestamp: int,
                 gas_limit:int,
                 chain_id:int, 
                 base_fee:int,
                 self_balance:int,
                 external_contracts:dict
                 ) -> None:
                 
        self.block_hash = block_hash.to_bytes(32, byteorder = 'big')
        self.block_number = block_number
        self.block_difficulty = block_difficulty
        self.coinbase = coinbase.to_bytes(20, byteorder = 'big')
        self.timestamp = timestamp
        self.gas_limit = gas_limit
        self.chain_id = chain_id
        self.base_fee = base_fee
        self.self_balance = self_balance
        self.external_contracts = external_contracts
        
