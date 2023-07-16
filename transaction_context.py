


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
        self.caller_address = (caller_address.to_bytes(20, byteorder = 'big')) if type(caller_address) == int else caller_address
        self.to_address = (to_address.to_bytes(20, byteorder = 'big')) if type(to_address) == int else to_address
        self.origin_address =  (origin_address.to_bytes(20, byteorder = 'big')) if type(origin_address) == int else origin_address
        self.value = value
        self.data = bytearray.fromhex(data) #if type(origin_address) == str else data
        self.gas_price = gas_price
        self.gas = gas
        self.nonce = nonce