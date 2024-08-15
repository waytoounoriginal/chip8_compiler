from .Tokens import Tokens
from .Types import (
    Literal,
    Label,
    Variable,
    Instruction
)
from .Globals import (
    variables_instance,
    labels_instance,
    raw_opcodes_instance
)

from .Interfaces import Bytecode

# Steps:
# 1. Load code and remove comments
# 2. Parse lines of code into instructions
# 3. Convert instructions into byecode

# Global address
CURRENT_ADDR: int = 0x200


def __remove_comments(code: str) -> str:
    """
    Removes the comments from the .chip8 file. Comments are defined by the ";" token
    :param code: str
    :return: list[str]
    """
    code: list[str] = code.splitlines()
    new_code: list[str] = []

    for line in code:
        line = line.strip()
        if line == "":
            continue

        if Tokens.COMMENT_TOKEN not in line:
            new_code.append(line)
            continue

        # If the whole line is a comment
        if line[0] == Tokens.COMMENT_TOKEN:
            # Skip the line
            continue

        final_index: int = line.index(Tokens.COMMENT_TOKEN)
        line = line[:final_index].strip()

        new_code.append(line)

    return "\n".join(new_code)


def __parse_code_segment(code: str):
    global CURRENT_ADDR

    code_lines: list[str] = code.splitlines()

    for line in code_lines:

        # print("CURRENT LINE:", line)

        # Try to get an instruction
        # If the line is an instruction
        curr_instr = Instruction.parse_definition(line, CURRENT_ADDR) or \
                     Label.parse_definition(line, CURRENT_ADDR) or \
                     Variable.parse_definition(line, CURRENT_ADDR) or \
                     Literal.parse_value(line)

        # Shouldn't be None
        if curr_instr is None:
            raise Exception("Invalid syntax present! "
                            f"Line in question: {line}")
        # Add the address
        if isinstance(curr_instr, Bytecode):
            codes = raw_opcodes_instance()
            codes.append(curr_instr)

            # Increment the current address of the program
            CURRENT_ADDR += curr_instr.byte_length()

        # print("CURRENT ADDR: ", hex(CURRENT_ADDR))


def __parse_code(code: str) -> bool:
    """
    Function parses the code into Segments and Instructions. Returns True if code is parsable, False otherwise
    :param code:
    :return: bool
    """

    # Remove comments
    code = __remove_comments(code)

    # print(code)

    # print(code)

    def __get_segment_code(segment: str) -> str:
        code_lines = code.splitlines()
        seg_start = code_lines.index(f"{Tokens.SEGMENT_BEGIN_TOKEN} {segment}{Tokens.DECLARATION_END_TOKEN}")
        seg_end = code_lines[seg_start + 1:].index(Tokens.SEGMENT_END_TOKEN)
        return "\n".join(code_lines[seg_start + 1:seg_start + seg_end + 1])

    code_segment_code: str = ""
    try:
        code_segment_code = __get_segment_code("code")
    except ValueError as e:
        print(e)
        return False

    # print(code_segment_code)

    # Parse the code group
    __parse_code_segment(code=code_segment_code)

    # Set the data segment
    data_segment_code: str = ""
    try:
        data_segment_code = __get_segment_code("data")
    except ValueError as e:
        print(e)
        return False

    # Parse the data
    __parse_code_segment(code=data_segment_code)

    # Final check on labels, variables, to see if they have an address
    variables = variables_instance()
    labels = labels_instance()

    # print("VARIABLES: ", variables)
    # print("LABELS: ", labels)

    for _, variable in variables.items():
        if variable.address is None:
            return False

    for _, label in labels.items():
        if label.address is None:
            return False

    return True


def __reset_instances() -> None:
    """
    Resets all prior instances of variables
    :return:
    """
    global CURRENT_ADDR

    vars = variables_instance()
    labels = labels_instance()
    opcodes = raw_opcodes_instance()

    vars.clear()
    labels.clear()
    opcodes.clear()
    CURRENT_ADDR = 0x200


def parse_file(file_path: str) -> bytes:
    """
    Parses the .chip8 file. Returns a list of bytes
    :param file_path:
    :return:
    """

    # Reset all prior instances
    __reset_instances()

    code: str = ""
    with open(file_path, "r") as f:
        code = "\n".join(f.readlines())

    valid_code: bool = __parse_code(code)

    if valid_code is False:
        print("Invalid code!")
        return b''

    # Print the raw instructions
    opcodes = raw_opcodes_instance()
    bytecodes = [opcode.to_bytes() for opcode in opcodes]

    return b''.join(bytecodes)
