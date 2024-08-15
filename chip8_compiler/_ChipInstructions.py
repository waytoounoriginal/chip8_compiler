from typing import TYPE_CHECKING, Callable, Type
if TYPE_CHECKING:
    from .Types import (
        Register,
        Literal
    )

from .Interfaces import InstructionsLUTEntry

# This namespace is meant to hide the LUTs and chip instructions.
# It is very ugly on purpose. Deal with it


# Generic functions - will return an int that will then be parsed into bytes
# We are using *args as a means to pass all 3 operands as parameters
def __no_operand(instruction_code: int, *args) -> int:
    return instruction_code


def __one_operand_addr(instruction_code: int, operand1: 'Literal', *args) -> int:
    __addr = operand1.value
    return instruction_code | (__addr & 0x0FFF)


def __one_operand_normal_reg(instruction_code: int, operand1: 'Register', *args) -> int:
    return instruction_code | (operand1.name << 8)


def __two_operand_nreg_nreg(instruction_code: int, operand1: 'Register', operand2: 'Register', *args) -> int:
    return instruction_code | (operand1.name << 8) | (operand2.name << 4)


def __two_operand_nreg_i(instruction_code: int, operand1: 'Register', operand2: 'Register', *args) -> int:
    return instruction_code | (operand1.name << 8)


def __two_operand_nreg_addr(instruction_code: int, operand1: 'Register', operand2: 'Literal', *args) -> int:
    __addr = operand2.value
    return instruction_code | (__addr & 0x0FFF)


def __two_operand_nreg_byte(instruction_code: int, operand1: 'Register', operand2: 'Literal', *args) -> int:
    operand_byte = operand2.value & 0x00FF
    return instruction_code | (operand1.name << 8) | operand_byte


def __two_operand_i_nreg(instruction_code: int, operand1: 'Register', operand2: 'Register', *args) -> int:
    return instruction_code | (operand2.name << 8)


def __two_operand_i_addr(instruction_code: int, operand1: 'Register', operand2: 'Literal', *args) -> int:
    __addr = operand2.value
    return instruction_code | (__addr & 0x0FFF)


def __drw(instruction_code: int, operand1: 'Register', operand2: 'Register', operand3: 'Literal', *args) -> int:
    return instruction_code | (operand1.name << 8) | (operand2.name << 4) | (operand3.value & 0x000F)


# Special instructions
__DRW_OPCODE = 0xD000
__DRW_FUNCTION = __drw

__LD_RI_OPCODE = 0xF065
__LD_RI_FUNCTION = __two_operand_nreg_i

# Special registers
__LD_RDT_OPCODE = 0xF007
__LD_RDT_FUNCTION = __two_operand_nreg_i

__LD_RK_OPCODE = 0xF00A
__LD_RK_FUNCTION = __two_operand_nreg_i

__LD_DTR_OPCODE = 0xF015
__LD_DTR_FUNCTION = __two_operand_i_nreg

__LD_STR_OPCODE = 0xF018
__LD_STR_FUNCTION = __two_operand_i_nreg

__LD_FR_OPCODE = 0xF029
__LD_FR_FUNCTION = __two_operand_i_nreg

__LD_BR_OPCODE = 0xF033
__LD_BR_FUNCTION = __two_operand_i_nreg

__NORMAL_INSTRUCTIONS_LUT: dict = {
    "NOOP": InstructionsLUTEntry(
        command_code=0x0000,
        func=__no_operand
    ),
    "CLS": InstructionsLUTEntry(
        command_code=0x00E0,
        func=__no_operand
    ),
    "RET": InstructionsLUTEntry(
        command_code=0x00EE,
        func=__no_operand
    ),
    "SYS": {
        "Literal": InstructionsLUTEntry(
            command_code=0x0000,
            func=__one_operand_addr
        )
    },
    "JP": {
        "Literal": InstructionsLUTEntry(
            command_code=0x1000,
            func=__one_operand_addr
        ),
        "Register": {
            "Literal": InstructionsLUTEntry(
                command_code=0xB000,
                func=__two_operand_nreg_addr
            )
        }
    },
    "CALL": {
        "Literal": InstructionsLUTEntry(
            command_code=0x2000,
            func=__one_operand_addr
        )
    },
    "SE": {
        "Register": {
            "Literal": InstructionsLUTEntry(
                command_code=0x3000,
                func=__two_operand_nreg_byte
            ),
            "Register": InstructionsLUTEntry(
                command_code=0x5000,
                func=__two_operand_nreg_nreg
            )
        }
    },
    "SNE": {
        "Register": {
            "Literal": InstructionsLUTEntry(
                command_code=0x4000,
                func=__two_operand_nreg_byte
            ),
            "Register": InstructionsLUTEntry(
                command_code=0x9000,
                func=__two_operand_nreg_nreg
            )
        }
    },
    "LD": {
        "Register": {
            "Literal": InstructionsLUTEntry(
                0x6000,
                __two_operand_nreg_byte
            ),
            "Register": InstructionsLUTEntry(
                0x8000,
                __two_operand_nreg_nreg
            )
        }
    },
    "ADD": {
        "Register": {
            "Literal": InstructionsLUTEntry(
                0x7000,
                __two_operand_nreg_byte
            ),
            "Register": InstructionsLUTEntry(
                0x8004,
                __two_operand_nreg_nreg
            )
        }
    },
    "OR": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x8001,
                __two_operand_nreg_nreg
            )
        }
    },
    "AND": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x8002,
                __two_operand_nreg_nreg
            )
        }
    },
    "XOR": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x8003,
                __two_operand_nreg_nreg
            )
        }
    },
    "SUB": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x8005,
                __two_operand_nreg_nreg
            )
        }
    },
    "SHR": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x8006,
                __two_operand_nreg_nreg
            )
        }
    },
    "SUBN": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x8007,
                __two_operand_nreg_nreg
            )
        }
    },
    "SHL": {
        "Register": {
            "Register": InstructionsLUTEntry(
                0x800E,
                __two_operand_nreg_nreg
            )
        }
    },
    "RND": {
        "Register": {
            "Literal": InstructionsLUTEntry(
                0xC000,
                __two_operand_nreg_byte
            )
        }
    },
    "SKP": {
        "Register": InstructionsLUTEntry(
            0xE09E,
            __one_operand_normal_reg
        )
    },
    "SKNP": {
        "Register": InstructionsLUTEntry(
            0xE0A1,
            __one_operand_normal_reg
        )
    },
}

__SPECIAL_INSTRUCTIONS_LUT: dict = {
            "LD": {
                "I": {
                    "Register": {
                        "Literal": InstructionsLUTEntry(
                            0xA000,
                            __two_operand_i_addr
                        ),
                        "Register": InstructionsLUTEntry(
                            0xF055,
                            __two_operand_i_nreg
                        )
                    }
                },
                "DT": {
                    "Register": {
                        "Register": InstructionsLUTEntry(
                            __LD_DTR_OPCODE,
                            __LD_DTR_FUNCTION
                        )
                    }
                },
                "ST": {
                    "Register": {
                        "Register": InstructionsLUTEntry(
                            __LD_STR_OPCODE,
                            __LD_STR_FUNCTION
                        )
                    }
                },
                "F": {
                    "Register": {
                        "Register": InstructionsLUTEntry(
                            __LD_FR_OPCODE,
                            __LD_FR_FUNCTION
                        )
                    }
                },
                "B": {
                    "Register": {
                        "Register": InstructionsLUTEntry(
                            __LD_BR_OPCODE,
                            __LD_BR_FUNCTION
                        )
                    }
                }

            },
            "ADD": {
                "I": {
                    "Register": {
                        "Register": InstructionsLUTEntry(
                            0xF01E,
                            __two_operand_i_nreg
                        )
                    }
                }
            }
        }

__EDGE_NREG_SREG_CASE: dict = {
    "LD": {
        # Second register name
        "I": InstructionsLUTEntry(
            command_code=__LD_RI_OPCODE,
            func=__LD_RI_FUNCTION
        ),
        "DT": InstructionsLUTEntry(
            command_code=__LD_RDT_OPCODE,
            func=__LD_RDT_FUNCTION
        ),
        "K": InstructionsLUTEntry(
            command_code=__LD_RK_OPCODE,
            func=__LD_RK_FUNCTION
        )
    }
}


# Public functions
def get_drw_entry() -> InstructionsLUTEntry:
    return InstructionsLUTEntry(
        command_code=__DRW_OPCODE,
        func=__DRW_FUNCTION
    )


def get_special_entry(
        command_name: str,
        register1_name: str,
        operand1_type: Type,
        operand2_type: Type
) -> InstructionsLUTEntry:
    # Convert the types to strings
    op1_type_str: str = operand1_type.__name__
    op2_type_str: str = operand2_type.__name__
    return __SPECIAL_INSTRUCTIONS_LUT[command_name][register1_name][op1_type_str][op2_type_str]


def get_edge_entry(
        command_name: str,
        register2_name: str
) -> InstructionsLUTEntry:
    return __EDGE_NREG_SREG_CASE[command_name][register2_name]


def get_normal_entry(
        command_name: str,
        operand1_type: Type,
        operand2_type: Type
) -> InstructionsLUTEntry:
    # Test if command has no operands
    NoneType: str = "NoneType"

    # Convert the types to strings
    op1_type_str: str = operand1_type.__name__
    op2_type_str: str = operand2_type.__name__

    if op1_type_str == NoneType:
        return __NORMAL_INSTRUCTIONS_LUT[command_name]

    # Test for the second operand
    if op2_type_str == NoneType:
        return __NORMAL_INSTRUCTIONS_LUT[command_name][op1_type_str]

    return __NORMAL_INSTRUCTIONS_LUT[command_name][op1_type_str][op2_type_str]

