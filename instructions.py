

class Instruction:
    def __init__(self, opcode: int, name: str):
        self.opcode = opcode
        self.name = name

    def execute(self, executor: Executor) -> None:
        raise NotImplementedError
