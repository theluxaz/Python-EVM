from typing import Optional
from instructions import Instructions
from execution_context import ExecutionContext
from transaction_context import TransactionContext
from state import State
from opcode_list import opcodes_list


# TODO This file needs heavy refactoring
class Executor:
    def __init__(
        self,
        contract_instance,
        bytecode: bytearray,
        execution_context: ExecutionContext,
        transaction_context: TransactionContext,
        EVM_STATE: State,
        static: Optional[bool] = False,
    ) -> None:
        self.address = transaction_context.to_address.hex()
        self.self_state = EVM_STATE.get(transaction_context.to_address.hex())
        self.contract_instance = contract_instance
        if self.self_state:
            self.instructions = Instructions(self, self.self_state["state"])
        else:
            self.instructions = Instructions(self, False)
        self.bytecode = bytecode
        self.execution_context = execution_context
        self.transaction_context = transaction_context
        self.EVM_STATE = EVM_STATE
        self.gas_remaining = transaction_context.gas
        self.gas_starting = transaction_context.gas
        self.return_data = None
        self.logs = []
        self.pc = 0
        self.static = static
        self.stopped = False
        self.finished = False
        self.reverted = False
        self.returned = False
        self.invalid = False

    # main processing loop
    def run(self):
        while (
            not self.stopped
            and not self.reverted
            and not self.returned
            and not self.finished
        ):
            print("")
            instruction = self.get_next_opcode()
            self.gas_remaining = self.gas_remaining - instruction["gas"]
            if self.pc > len(self.bytecode):
                print("CODE FINISHED - STOPPING")
                print()
                self.finished = True
                return "EXECUTION FINISHED"
            # TODO ADD PROPER GAS ERRORS - ENABLE LATER AFTER TESTING
            elif self.gas_remaining < 0:
                print("OUT OF GAS - STOPPING")
                print()
                self.stopped = True
                return "OUT OF GAS"

            print(f"Opcode Instruction  is : {instruction}")

            processing_function = self.instructions.get_instruction_function(
                instruction["name"]
            )
            result = processing_function()
            self.instructions.stack.print()

            if self.returned or self.reverted:
                return result
            elif self.stopped or self.finished:
                # TODO IMPLEMENT STOPPED FUNCTIONALITY
                print("STOPPED PROGRAM")
                return "STOPPED"
            elif self.invalid:
                # TODO IMPLEMENT INVALID FUNCTIONALITY
                print("INVALID VALUE STOPPED PROGRAM")
                return "INVALID"

    def revert_transaction(self):
        self.transaction_context.gas = self.gas_remaining
        if not self.static:
            state_dict = self.EVM_STATE.get(self.address)
            if state_dict:
                state_dict["balance"] = state_dict["balance"] + (
                    self.transaction_context.value
                )
                state_dict["balance"] = state_dict["balance"] - (
                    self.gas_starting - self.gas_remaining
                )
                self.EVM_STATE.set(self.address, state_dict)

    def consume_gas(self):
        self.transaction_context.gas = self.gas_remaining
        if not self.static:
            state_dict = self.EVM_STATE.get(self.address)
            if state_dict:
                state_dict["balance"] = state_dict["balance"] - (
                    self.gas_starting - self.gas_remaining
                )
                self.EVM_STATE.set(self.address, state_dict)

    def finish_transaction(self):
        self.transaction_context.gas = self.gas_remaining
        if not self.static:
            state_dict = self.EVM_STATE.get(self.address)
            if state_dict:
                state_dict["balance"] = state_dict["balance"] + (
                    self.transaction_context.value
                )
                state_dict["balance"] = state_dict["balance"] - (
                    self.gas_starting - self.gas_remaining
                )
                state_dict["state"] = self.instructions.storage.storage
                self.EVM_STATE.set(self.address, state_dict)

    def update_nonce(self):
        self.transaction_context.nonce = self.transaction_context.nonce + 1

    def process_bytecode(self, next_word) -> bytes:
        item = self.bytecode[self.pc : self.pc + next_word]
        self.pc += next_word
        return item

    def get_next_opcode(self):
        mnemonic = self.process_bytecode(1)
        opcode = [
            x
            for x in opcodes_list
            if x["mnemonic"] == int.from_bytes(mnemonic, byteorder="big")
        ][0]
        return opcode

    def check_opcode_at_pc(self, offset):
        if offset >= len(self.bytecode):
            return None
        mnemonic = self.bytecode[offset : offset + 1]
        print(str(self.bytecode))
        print(
            f"Byte offset at {offset} is {mnemonic} or mnemonic {int.from_bytes(mnemonic, byteorder='big')} pc is {self.pc}, len of bytecode is {len(self.bytecode)}"
        )
        opcode = [
            x
            for x in opcodes_list
            if x["mnemonic"] == int.from_bytes(mnemonic, byteorder="big")
        ][0]
        return opcode

    def set_pc(self, pc):
        self.pc = pc
        return pc

    def print_logs(self):
        for log in self.logs:
            print(
                f"Log: address={log['address']}   topics={get_bytearray_list_to_string(log['topics'])}   data={log['data']}"
            )

    # Checks if the jump destination is a value used by push and not opcode instruction
    def is_opcode_valid(self, jump_target_position):
        for i in range(1, 32):
            mnemonic = self.bytecode[
                jump_target_position - i : jump_target_position + 1 - i
            ]
            opcode = [
                x
                for x in opcodes_list
                if x["mnemonic"] == int.from_bytes(mnemonic, byteorder="big")
            ]
            if opcode:
                opcode = opcode[0]
                # Checks if PUSH was previously and number unusable
                if "PUSH" + str(i) == opcode["name"]:
                    return False

        return True


def get_bytearray_list_to_string(data_array):
    result = ""
    if data_array:
        for item in data_array:
            if len(result) > 1:
                result += ", "
            result += item
    return result
