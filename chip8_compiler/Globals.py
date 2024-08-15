from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .Types import (
        Variable,
        Bytecode,
        Label,
        Instruction,
        Literal
    )

# Global variables to be used by the parsing tools
__VARIABLES__: dict[str, 'Variable'] = {}
__LABELS__: dict[str, 'Label'] = {}
__RAW_OPCODES__: list['Bytecode'] = []


def variables_instance() -> dict[str, 'Variable']:
    global __VARIABLES__
    return __VARIABLES__


def labels_instance() -> dict[str, 'Label']:
    global __LABELS__
    return __LABELS__


def raw_opcodes_instance() -> list['Bytecode']:
    global __RAW_OPCODES__
    return __RAW_OPCODES__
