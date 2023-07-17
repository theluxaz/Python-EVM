opcodes_list = [
    {"name":"STOP",
    "mnemonic":0x00,
    "gas":0
    },


    {"name":"ADD",
    "mnemonic":0x01,
    "gas":3
    },
    {"name":"MUL",
    "mnemonic":0x02,
    "gas":5
    },
    {"name":"SUB",
    "mnemonic":0x03,
    "gas":3
    },
    {"name":"DIV",
    "mnemonic":0x04,
    "gas":2
    },
    {"name":"SDIV",
    "mnemonic":0x05,
    "gas":5
    },
    {"name":"MOD",
    "mnemonic":0x06,
    "gas":5
    },
    {"name":"SMOD",
    "mnemonic":0x07,
    "gas":5
    },
    {"name":"ADDMOD",
    "mnemonic":0x08,
    "gas":8
    },
    {"name":"MULMOD",
    "mnemonic":0x09,
    "gas":8
    },
    {"name":"EXP",
    "mnemonic":0x0A,
    "gas":10
    },
    {"name":"SIGNEXTEND",
    "mnemonic":0x0B,
    "gas":5
    },


    {"name":"LT",
    "mnemonic":0x10,
    "gas":3
    },
    {"name":"GT",
    "mnemonic":0x11,
    "gas":3
    },
    {"name":"SLT",
    "mnemonic":0x12,
    "gas":3
    },
    {"name":"SGT",
    "mnemonic":0x13,
    "gas":3
    },
    {"name":"EQ",
    "mnemonic":0x14,
    "gas":3
    },
    {"name":"ISZERO",
    "mnemonic":0x15,
    "gas":3
    },
    {"name":"AND",
    "mnemonic":0x16,
    "gas":3
    },
    {"name":"OR",
    "mnemonic":0x17,
    "gas":3
    },
    {"name":"XOR",
    "mnemonic":0x18,
    "gas":3
    },
    {"name":"NOT",
    "mnemonic":0x19,
    "gas":3
    },
    {"name":"BYTE",
    "mnemonic":0x1A,
    "gas":3
    },
    {"name":"SHL",
    "mnemonic":0x1B,
    "gas":3
    },
    {"name":"SHR",
    "mnemonic":0x1C,
    "gas":3
    },
    {"name":"SAR",
    "mnemonic":0x1D,
    "gas":3
    },
    

    {"name":"SHA3",
    "mnemonic":0x20,
    "gas":30
    },


    {"name":"ADDRESS",
    "mnemonic":0x30,
    "gas":2
    },
    {"name":"BALANCE",
    "mnemonic":0x31,
    "gas":100
    },
    {"name":"ORIGIN",
    "mnemonic":0x32,
    "gas":2
    },
    {"name":"CALLER",
    "mnemonic":0x33,
    "gas":2
    },
    {"name":"CALLVALUE",
    "mnemonic":0x34,
    "gas":2
    },
    {"name":"CALLDATALOAD",
    "mnemonic":0x35,
    "gas":3
    },
    {"name":"CALLDATASIZE",
    "mnemonic":0x36,
    "gas":2
    },
    {"name":"CALLDATACOPY",
    "mnemonic":0x37,
    "gas":3
    },
    {"name":"CODESIZE",
    "mnemonic":0x38,
    "gas":2
    },
    {"name":"CODECOPY",
    "mnemonic":0x39,
    "gas":3
    },
    {"name":"GASPRICE",
    "mnemonic":0x3A,
    "gas":2
    },
    {"name":"EXTCODESIZE",
    "mnemonic":0x3B,
    "gas":100
    },
    {"name":"EXTCODECOPY",
    "mnemonic":0x3C,
    "gas":100
    },
    {"name":"RETURNDATASIZE",
    "mnemonic":0x3D,
    "gas":2
    },
    {"name":"RETURNDATACOPY",
    "mnemonic":0x3E,
    "gas":3
    },
    {"name":"EXTCODEHASH",
    "mnemonic":0x3F,
    "gas":2
    },


    {"name":"BLOCKHASH",
    "mnemonic":0x40,
    "gas":20
    },
    {"name":"COINBASE",
    "mnemonic":0x41,
    "gas":2
    },
    {"name":"TIMESTAMP",
    "mnemonic":0x42,
    "gas":2
    },
    {"name":"NUMBER",
    "mnemonic":0x43,
    "gas":2
    },
    {"name":"PREVRANDAO",
    "mnemonic":0x44,
    "gas":2
    },
    {"name":"GASLIMIT",
    "mnemonic":0x45,
    "gas":2
    },
    {"name":"CHAINID",
    "mnemonic":0x46,
    "gas":2
    },
    {"name":"SELFBALANCE",
    "mnemonic":0x47,
    "gas":5
    },
    {"name":"BASEFEE",
    "mnemonic":0x48,
    "gas":2
    },

    
    {"name":"POP",
    "mnemonic":0x50,
    "gas":2
    },
    {"name":"MLOAD",
    "mnemonic":0x51,
    "gas":3
    },
    {"name":"MSTORE",
    "mnemonic":0x52,
    "gas":3
    },
    {"name":"MSTORE8",
    "mnemonic":0x53,
    "gas":3
    },
    {"name":"SLOAD",
    "mnemonic":0x54,
    "gas":100
    },
    {"name":"SSTORE",
    "mnemonic":0x55,
    "gas":100
    },
    {"name":"JUMP",
    "mnemonic":0x56,
    "gas":8
    },
    {"name":"JUMPI",
    "mnemonic":0x57,
    "gas":10
    },
    {"name":"PC",
    "mnemonic":0x58,
    "gas":2
    },
    {"name":"MSIZE",
    "mnemonic":0x59,
    "gas":2
    },
    {"name":"GAS",
    "mnemonic":0x5A,
    "gas":2
    },
    {"name":"JUMPDEST",
    "mnemonic":0x5B,
    "gas":1
    },
    {"name":"PUSH0",
    "mnemonic":0x5F,
    "gas":2
    },


    {"name":"PUSH1",
    "mnemonic":0x60,
    "gas":3
    },
    {"name":"PUSH2",
    "mnemonic":0x61,
    "gas":3
    },
    {"name":"PUSH3",
    "mnemonic":0x62,
    "gas":3
    },
    {"name":"PUSH4",
    "mnemonic":0x63,
    "gas":3
    },
    {"name":"PUSH5",
    "mnemonic":0x64,
    "gas":3
    },
    {"name":"PUSH6",
    "mnemonic":0x65,
    "gas":3
    },
    {"name":"PUSH7",
    "mnemonic":0x66,
    "gas":3
    },
    {"name":"PUSH8",
    "mnemonic":0x67,
    "gas":3
    },
    {"name":"PUSH9",
    "mnemonic":0x68,
    "gas":3
    },
    {"name":"PUSH10",
    "mnemonic":0x69,
    "gas":3
    },
    {"name":"PUSH11",
    "mnemonic":0x6A,
    "gas":3
    },
    {"name":"PUSH12",
    "mnemonic":0x6B,
    "gas":3
    },
    {"name":"PUSH13",
    "mnemonic":0x6C,
    "gas":3
    },
    {"name":"PUSH14",
    "mnemonic":0x6D,
    "gas":3
    },
    {"name":"PUSH15",
    "mnemonic":0x6E,
    "gas":3
    },
    {"name":"PUSH16",
    "mnemonic":0x6F,
    "gas":3
    },


    {"name":"PUSH17",
    "mnemonic":0x70,
    "gas":3
    },
    {"name":"PUSH18",
    "mnemonic":0x71,
    "gas":3
    },
    {"name":"PUSH19",
    "mnemonic":0x72,
    "gas":3
    },
    {"name":"PUSH20",
    "mnemonic":0x73,
    "gas":3
    },
    {"name":"PUSH21",
    "mnemonic":0x74,
    "gas":3
    },
    {"name":"PUSH22",
    "mnemonic":0x75,
    "gas":3
    },
    {"name":"PUSH23",
    "mnemonic":0x76,
    "gas":3
    },
    {"name":"PUSH24",
    "mnemonic":0x77,
    "gas":3
    },
    {"name":"PUSH25",
    "mnemonic":0x78,
    "gas":3
    },
    {"name":"PUSH26",
    "mnemonic":0x79,
    "gas":3
    },
    {"name":"PUSH27",
    "mnemonic":0x7A,
    "gas":3
    },
    {"name":"PUSH28",
    "mnemonic":0x7B,
    "gas":3
    },
    {"name":"PUSH29",
    "mnemonic":0x7C,
    "gas":3
    },
    {"name":"PUSH30",
    "mnemonic":0x7D,
    "gas":3
    },
    {"name":"PUSH31",
    "mnemonic":0x7E,
    "gas":3
    },
    {"name":"PUSH32",
    "mnemonic":0x7F,
    "gas":3
    },


    {"name":"DUP1",
    "mnemonic":0x80,
    "gas":3
    },
    {"name":"DUP2",
    "mnemonic":0x81,
    "gas":3
    },
    {"name":"DUP3",
    "mnemonic":0x82,
    "gas":3
    },
    {"name":"DUP4",
    "mnemonic":0x83,
    "gas":3
    },
    {"name":"DUP5",
    "mnemonic":0x84,
    "gas":3
    },
    {"name":"DUP6",
    "mnemonic":0x85,
    "gas":3
    },
    {"name":"DUP7",
    "mnemonic":0x86,
    "gas":3
    },
    {"name":"DUP8",
    "mnemonic":0x87,
    "gas":3
    },
    {"name":"DUP9",
    "mnemonic":0x88,
    "gas":3
    },
    {"name":"DUP10",
    "mnemonic":0x89,
    "gas":3
    },
    {"name":"DUP11",
    "mnemonic":0x8A,
    "gas":3
    },
    {"name":"DUP12",
    "mnemonic":0x8B,
    "gas":3
    },
    {"name":"DUP13",
    "mnemonic":0x8C,
    "gas":3
    },
    {"name":"DUP14",
    "mnemonic":0x8D,
    "gas":3
    },
    {"name":"DUP15",
    "mnemonic":0x8E,
    "gas":3
    },
    {"name":"DUP16",
    "mnemonic":0x8F,
    "gas":3
    },


    {"name":"SWAP1",
    "mnemonic":0x90,
    "gas":3
    },
    {"name":"SWAP2",
    "mnemonic":0x91,
    "gas":3
    },
    {"name":"SWAP3",
    "mnemonic":0x92,
    "gas":3
    },
    {"name":"SWAP4",
    "mnemonic":0x93,
    "gas":3
    },
    {"name":"SWAP5",
    "mnemonic":0x94,
    "gas":3
    },
    {"name":"SWAP6",
    "mnemonic":0x95,
    "gas":3
    },
    {"name":"SWAP7",
    "mnemonic":0x96,
    "gas":3
    },
    {"name":"SWAP8",
    "mnemonic":0x97,
    "gas":3
    },
    {"name":"SWAP9",
    "mnemonic":0x98,
    "gas":3
    },
    {"name":"SWAP10",
    "mnemonic":0x99,
    "gas":3
    },
    {"name":"SWAP11",
    "mnemonic":0x9A,
    "gas":3
    },
    {"name":"SWAP12",
    "mnemonic":0x9B,
    "gas":3
    },
    {"name":"SWAP13",
    "mnemonic":0x9C,
    "gas":3
    },
    {"name":"SWAP14",
    "mnemonic":0x9D,
    "gas":3
    },
    {"name":"SWAP15",
    "mnemonic":0x9E,
    "gas":3
    },
    {"name":"SWAP16",
    "mnemonic":0x9F,
    "gas":3
    },


    {"name":"LOG0",
    "mnemonic":0xA0,
    "gas":375
    },
    {"name":"LOG1",
    "mnemonic":0xA1,
    "gas":750
    },
    {"name":"LOG2",
    "mnemonic":0xA2,
    "gas":1125
    },
    {"name":"LOG3",
    "mnemonic":0xA3,
    "gas":1500
    },
    {"name":"LOG4",
    "mnemonic":0xA4,
    "gas":1875
    },


    {"name":"CREATE",
    "mnemonic":0xF0,
    "gas":32000
    },
    {"name":"CALL",
    "mnemonic":0xF1,
    "gas":100
    },
    {"name":"CALLCODE",
    "mnemonic":0xF2,
    "gas":100
    },
    {"name":"RETURN",
    "mnemonic":0xF3,
    "gas":0
    },
    {"name":"DELEGATECALL",
    "mnemonic":0xF4,
    "gas":100
    },
    {"name":"CREATE2",
    "mnemonic":0xF5,
    "gas":32000
    },
    {"name":"STATICCALL",
    "mnemonic":0xFA,
    "gas":100
    },
    {"name":"REVERT",
    "mnemonic":0xFD,
    "gas":0
    },
    {"name":"INVALID",
    "mnemonic":0xFE,
    "gas":0
    },
    {"name":"SELFDESTRUCT",
    "mnemonic":0xFF,
    "gas":5000
    },





]


