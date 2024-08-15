from enum import StrEnum


# Maybe some tokens could have a better name
class Tokens(StrEnum):
    COMMENT_TOKEN = ";",
    WHITESPACE_TOKEN = ' ',
    SEPARATOR_TOKEN = ',',
    ZERO_WIDTH_TOKEN = "",
    LABEL_NAME_TOKEN = "__",
    DECLARATION_END_TOKEN = ":",

    LABEL_TOKEN = "label",
    VARIABLE_TOKEN = "variable",

    SEGMENT_BEGIN_TOKEN = "segment",
    SEGMENT_END_TOKEN = "segment_end"

    LITERAL_TOKEN = "$",
    LITERAL_DECIMAL_TOKEN = "$d",
    LITERAL_BINARY_TOKEN = "$b",

    ADDRESS_SPECIAL_TOKEN = "__ADDR__"
