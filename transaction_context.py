


class TransactionContext:

    def __init__(self, caller_address: bytearray, 
                 to_address: bytearray, 
                 origin_address:bytearray,
                 value: int, 
                 data: bytearray, 
                 gas_price: int,
                 gas: int,
                 nonce: int,
                 ) -> None:
        self.caller_address = bytearray.fromhex(caller_address) if type(caller_address)== str else caller_address
        self.to_address = bytearray.fromhex(to_address) if type(to_address)== str else to_address
        self.origin_address = bytearray.fromhex(origin_address) if type(origin_address)== str else origin_address
        self.value = value
        self.data = bytearray.fromhex(data) #if type(origin_address) == str else data
        self.gas_price = gas_price
        self.gas = gas
        self.nonce = nonce