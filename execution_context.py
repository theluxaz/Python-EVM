from external_contract import ExternalContract


class ExecutionContext:

    def __init__(self, block_hash: bytearray, 
                 block_number:int,
                 block_prevrandao:int,
                 coinbase: bytearray, 
                 timestamp: int,
                 gas_limit:int,
                 chain_id:int, 
                 base_fee:int
                 ) -> None:
                 
        self.block_hash = bytearray.fromhex(block_hash)
        self.block_number = block_number
        self.block_prevrandao = block_prevrandao
        self.coinbase = bytearray.fromhex(coinbase)
        self.timestamp = timestamp
        self.gas_limit = gas_limit
        self.chain_id = chain_id
        self.base_fee = base_fee

        
        
        
