from typing import Union, TypeAlias, Callable, Any, Type
from dataclasses import dataclass

from .Globals import (
    variables_instance,
    labels_instance
)

from .Tokens import (
    Tokens
)

from .Interfaces import (
    Bytecode,
    InstructionsLUTEntry
)

from ._ChipInstructions import (
    get_normal_entry,
    get_special_entry,
    get_edge_entry,
    get_drw_entry
)


@dataclass
class Literal(Bytecode):
    value: int

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(1, signed=False, byteorder="big")

    def __str__(self):
        return f"Literal({self.value})"

    @staticmethod
    def byte_length() -> int:
        return 1

    @staticmethod
    def parse_value(val: str) -> Union["Literal", None]:
        """
        Parses the literal variable. In case it is not a literal, return None
        :param val: str
        :return: int | None
        """
        beg_char: str = val[0]

        # Literal test
        if beg_char != Tokens.LITERAL_TOKEN:
            # We will return NONE
            return None

        first_chars: str = val[:2]
        # Decimal and binary tests
        if first_chars == Tokens.LITERAL_DECIMAL_TOKEN:
            return Literal(value=int(val[2:]))
        elif first_chars == Tokens.LITERAL_BINARY_TOKEN:
            return Literal(value=int(val[2:], 2))

        return Literal(value=int(val[1:], 16))


@dataclass
class Label:
    """
    The Label class. Initially has the address unset, until the parser sets it.
    """
    name: str
    address: int | None = None

    def __str__(self):
        return f"Label({self.name}, at {hex(self.address)})"

    @staticmethod
    def parse_value(val: str) -> Union["Label", None]:
        """
        Parses the Label value. Returns None if not a Label
        :param val
        :return:
        """
        if val[:2] != Tokens.LABEL_NAME_TOKEN:
            return None

        # Get the global state
        global_state = labels_instance()

        # See if the label already exists
        global_label: Label | None = global_state.get(val, None)

        if global_label is not None:
            return global_label

        # Add the label into the labels instance
        label: Label = Label(name=val)

        global_state[val] = label
        return label

    @staticmethod
    def parse_definition(line: str, address: int) -> Union['Label', None]:
        """
        Checks the code line for a label. Returns None in case of no label existing.

        In case of conflicting Label names, raises an Exception.
        :param line
        :param address
        :return:  Label | None
        """

        matches: list[str] = line.split(Tokens.WHITESPACE_TOKEN)

        if len(matches) != 2:
            return None

        label_keyword: str = matches[0]
        if label_keyword != Tokens.LABEL_TOKEN:
            return None

        name: str = matches[1]

        if name[-1] != Tokens.DECLARATION_END_TOKEN or name[:2] != Tokens.LABEL_NAME_TOKEN:
            return None

        name = name[:-1] # Gets the label name

        # The method adds a label into existence
        global_state = labels_instance()
        global_label: Label | None = global_state.get(name, None)

        # If it exists
        if global_label is not None:
            # Check if it was already defined
            if global_label.address is not None:
                raise Exception(f"Label '{name}' was already defined")
            else:
                global_label.address = address
                return global_label

        global_label = Label(
            name=name,
            address=address
        )

        global_state[name] = global_label
        return global_label


@dataclass
class Variable:
    """
    The Variable class. Initially has the address and value unset, until the parser sets it.
    """
    name: str
    value: Literal = None
    address: int | None = None

    def __str__(self):
        return f"""Variable(name={self.name}, value={self.value.__str__()}, at {hex(self.address)})"""

    @staticmethod
    def parse_value(val: str) -> 'Variable':
        """
        Parses the Variable. Always returns an unset variable
        :param val: str
        :param global_states
        :return:
        """

        global_state = variables_instance()
        global_var: Variable | None = global_state.get(val, None)

        if global_var is not None:
            return global_var

        # Add it onto the instance
        variable: Variable = Variable(
            name=val
        )

        global_state[val] = variable
        return variable

    @staticmethod
    def parse_definition(line: str, address: int) -> Union['Variable', None]:
        """
        Parses a code line to check for a variable. Returns None in case of no such thing.

        In case of conflicting variable names, raises an Exception
        :param line: str
        :param address
        :return: Variable | None
        """

        words: list[str] = line.split(Tokens.WHITESPACE_TOKEN)

        if len(words) != 3:
            return None

        variable_keyword: str = words[0]
        if variable_keyword != Tokens.VARIABLE_TOKEN:
            return None

        name: str = words[1]
        val: str = words[2]

        global_state = variables_instance()
        global_var: Variable | None = global_state.get(name, None)

        # Check if it exists
        if global_var is not None:
            if global_var.address is not None:
                raise Exception(f"Variable '{name}' was already defined")
            else:
                # print("Setting data for variable ", name)
                # print("Value: ", val),
                # print("Addr: ", current_address_instance())
                global_var.address = address
                global_var.value = Literal.parse_value(val)
                return global_var

        global_var = Variable(
            name=name,
            value=Literal.parse_value(val),
            address=address
        )

        global_state[name] = global_var
        return global_var


@dataclass
class Register:
    """
    A Register class.

    For simplicity's sake we are treating K, B, F, DT, ST as registers.
    """
    name: int | str | None
    is_special_reg: bool

    def __str__(self):
        return f"Register({self.name if self.is_special_reg else hex(self.name)})"

    @staticmethod
    def parse_value(val: str) -> Union["Register", None]:
        """
        Parses the register value. Returns None if not a Register
        :param val: str
        :return: Register | None
        """
        if val[0] not in ['V', 'I', 'K', 'B', 'F', 'R']:
            if val not in ["DT", "ST"]:
                return None

        if val[0] != 'V':
            return Register(name=val, is_special_reg=True)

        parsed_val: int = int(val[1:], 16)

        if parsed_val > 0xF:
            raise Exception(f"Invalid Register value for register '{val}'")

        return Register(
            name=parsed_val,
            is_special_reg=False
        )


@dataclass
class Instruction(Bytecode):
    command: str
    address: int
    operand1: Register | Label | Literal | None = None
    operand2: Register | Literal | Variable | None = None
    optional_operand: Literal | Variable | None = None # Used by DRW

    def __str__(self):
        return f"Instruction(\n"\
            f"\tcommand: {self.command},\n"\
            f"\toperand1: {self.operand1.__str__()}\n"\
            f"\toperand2: {self.operand2.__str__()}\n"\
            f"\toptional operand: {self.optional_operand.__str__()}\n"\
            f"\tbytecode: {self.to_bytes()},\n"\
            f"\tat {hex(self.address)}\n"\
            ")"

    def to_bytes(self) -> bytes:

        # We can finally return, based on the set parameters
        # Op code first

        # print("CHECKING FOR COMMAND", self.command)
        # print("WITH OPERAND 1", self.operand1)
        # print("OPERAND 2", self.operand2)
        # print("OPTIONAL OPERAND", self.optional_operand)
        # print()

        # We will convert each Label and Variable into a Literal
        operand1 = self.operand1
        operand2 = self.operand2
        operand3 = self.optional_operand

        # Print the types before
        # print("BEFORE TYPES: ", type(operand1), type(operand2), type(operand3))
        def get_operand_value(operand):
            if isinstance(operand, Variable):
                return operand.value
            elif isinstance(operand, Label):
                return Literal(operand.address)
            return operand

        operand1 = get_operand_value(operand1)
        operand2 = get_operand_value(operand2)
        operand3 = get_operand_value(operand3)

        # print("AFTER TYPES: ", type(operand1), type(operand2), type(operand3))

        # Drw Edge case
        if operand3 is not None:
            # DRW CASE
            entry: InstructionsLUTEntry = get_drw_entry()
            return entry.get_bytes(
                operand1,
                operand2,
                operand3
            )

        # Check if the first operand is a special register
        if type(operand1) == Register and operand1.is_special_reg:
            entry: InstructionsLUTEntry = get_special_entry(
                self.command,
                operand1.name,
                type(operand1),
                type(operand2)
            )
            return entry.get_bytes(
                operand1,
                operand2,
                operand3
            )

        # We have the special case cheked up.
        # We need to check the LD_RI case
        if type(operand1) == Register and type(operand2) == Register and operand2.is_special_reg == True:
            entry: InstructionsLUTEntry = get_edge_entry(
                command_name=self.command,
                register2_name=operand2.name
            )
            return entry.get_bytes(
                operand1,
                operand2,
                operand3
            )

        # Now we can check the generic cases
        entry: InstructionsLUTEntry = get_normal_entry(
            self.command,
            type(operand1),
            type(operand2)
        )
        return entry.get_bytes(
            operand1,
            operand2,
            operand3
        )

    @staticmethod
    def byte_length() -> int:
        return 2

    @staticmethod
    def parse_definition(
            line: str,
            address: int
    ) -> Union['Instruction', None]:
        """
        Function to parse line of code into Instruction. Returns None in case of an invalid syntax  or Literal
        :param line: str
        :param address
        :return: Instruction | None
        """

        # We will split the string by the spaces and get rid of the comma
        line = line.replace(Tokens.SEPARATOR_TOKEN, Tokens.ZERO_WIDTH_TOKEN)
        words: list[str] = line.split(Tokens.WHITESPACE_TOKEN)

        __INSTRUCTION_LIST: list[str] = [
            "SYS","CLS","RET","JP","CALL","SE","SNE","LD","ADD","OR","AND","XOR","SUB","SHR","SUBN","SHL","RND","DRW","SKP","SKNP","NOOP"
        ]

        if words[0] not in __INSTRUCTION_LIST:
            return None

        # print("INSTRUCTION STR: ", matches)

        # Create the instruction
        if len(words) == 1:
            return Instruction(command=words[0], address=address)
        elif len(words) == 2:

            # We will parse the second argument. It can be either a register, label or a literal
            if words[1] != Tokens.ADDRESS_SPECIAL_TOKEN:
                parsed_operand1_val = Register.parse_value(words[1]) or \
                                 Label.parse_value(words[1]) or \
                                 Literal.parse_value(words[1])
            else:
                parsed_operand1_val = Literal(value=address)

            # If it's still None return
            if parsed_operand1_val is None:
                return None

            return Instruction(
                command=words[0],
                operand1=parsed_operand1_val,
                address=address
            )

        # Parse the last argument
        # Regster first

        # if parsed_val is None:
        #     parsed_val = Literal.parse_value(matches[2])
        #
        #     if parsed_val is None:
        #         # Label test
        #         parsed_val = Label.parse_value(matches[2])
        #
        #         if parsed_val is None:
        #             # Variable test
        #             parsed_val = Variable.parse_value(matches[2])

        # Check if it isn't a token
        if words[2] != Tokens.ADDRESS_SPECIAL_TOKEN:
            parsed_operand2_val = Register.parse_value(words[2]) or \
                         Literal.parse_value(words[2]) or \
                         Label.parse_value(words[2]) or \
                         Variable.parse_value(words[2])
        else:
            parsed_operand2_val = Literal(value=address)

        # If it's still none, return None
        if parsed_operand2_val is None:
            return None

        instruction: Instruction = Instruction(
            command=words[0],
            operand1=Register.parse_value(words[1]),
            operand2=parsed_operand2_val,
            address=address
        )

        # Parse the optional argument
        if len(words) == 4:
            if words[-1] != Tokens.ADDRESS_SPECIAL_TOKEN:
                parsed_optional_val = Literal.parse_value(words[-1]) or Variable.parse_value(words[-1])
            else:
                parsed_optional_val = Literal(value=address)

            # If it's still None
            if parsed_optional_val is None:
                return None

            instruction.optional_operand = parsed_optional_val

        return instruction
