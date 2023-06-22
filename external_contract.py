

class ExternalContract:

    def __init__(self, address:bytes, bytecode:bytes) -> None:
        self.address = address
        self.bytecode = bytecode