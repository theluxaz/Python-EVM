
<!-- ABOUT THE PROJECT -->
## About The Project


This is a project to recreate EVM in Python from scratch. Please do not use this in production applications.




<!-- GETTING STARTED -->
## Getting Started



### Installation

1. Install Python 3.8+

2. Install required pip packages ("eth-hash","simple-rlp")
   ```sh
   pip install eth-hash
   pip install simple-rlp
   ```
3. Clone the repo
   ```sh
   git clone https://github.com/theluxaz/Python-EVM.git
   ```
4. Run run.py after inserting values
   ```sh
   python run.py
   ```




<!-- USAGE EXAMPLES -->
## Usage

To do later.

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->



<!-- ROADMAP -->
## Roadmap

#### EVM:

- [x] Stack
- [x] Memory
- [x] Storage
- [x] Gas (Static)
- [x] System     
- [x] Testing
<br/>

#### Opcodes:

- [x] Stop and Arithmetic Operations
- [x] Comparison & Bitwise Logic Operations
- [x] SHA3
- [x] Environmental Information
- [x] Block Information
- [x] Stack, Memory, Storage and Flow Operations
- [x] Push Operations
- [x] Duplication Operations
- [x] Exchange Operations
- [x] Logging Operations
- [x] System operations
- [x] Halt Execution, Mark for deletion Operations

<!-- FUTURE IMPROVEMENTS -->
## Future Improvements

* Add block header history for BLOCKHASH
* Blockchain persistence via Merkle Patricia Trie
* Dynamic Gas
* Add validation
* Errors for edge cases
* Refactor and clean code

<!-- DAILY -->
## Daily Progress

### Day 1: (June 15)
Set up architecture, file structure, listed all opcodes with their gas and mnemonics.

### Day 2: (June 19)
Implemented arithmetic, comparison and bitwise operation opcodes.

### Day 3: (June 20)
Implemented memory, storage, PUSH, DUP and SWAP opcodes.

### Day 4: (June 21)
Reworked stack to work with bytes, tested and fixed all the previously added opcode implementations. Added JUMP and GAS functionality.

### Day 5: (June 22)
Added functionality for both execution and transaction context. Added instruction related to them such as CALLDATACOPY or GASLIMIT. Added EXTCODESIZE, EXTCODECOPY and EXTCODEHASH.

### Day 6: (July 11)
Added functionality for ADDRESS and BALANCE. Added logging opcodes such as LOG0. Started refactoring the application to accommodate CREATE instructions.

### Day 7: (July 15)
Added functionality for testing opcodes from evm-from-scratch-challenge resources https://github.com/w1nt3r-eth/evm-from-scratch. Adjusted Executor to work with multiple contexts. Fixed errors present in certain opcode implementations.

### Day 8: (July 16)
Added many more opcodes which needed major refactoring, such as CALL, DELEGATECALL, RETURNDATACOPY etc. Reworked context nesting and reverting. Tested and fixed most implemented opcodes.

### Day 9: (July 16)
Finished all the remaining Opcodes such as CREATE, CREATE2 and SELFDESTRUCT. Made the EVM fully functional and tested. Code cleanup and refactoring needed.


<!-- LICENSE -->
## License

Distributed under the MIT License. 


