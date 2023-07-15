


class TransactionContext:

    def __init__(self, sender_address: bytearray, 
                 origin_address:bytearray,
                 value: int, 
                 data: bytearray, 
                 gas_price: int,
                 gas: int,
                 nonce: int,
                 ) -> None:
        self.sender_address = (sender_address.to_bytes(20, byteorder = 'big')) if type(sender_address) == int else sender_address
        self.origin_address =  (origin_address.to_bytes(20, byteorder = 'big')) if type(origin_address) == int else origin_address
        self.value = value
        self.data = data.to_bytes((data.bit_length() + 7) // 8, byteorder = 'big') if type(origin_address) == int else data
        self.gas_price = gas_price
        self.gas = gas
        self.nonce = nonce