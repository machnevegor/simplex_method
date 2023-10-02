from .token import TokenKind


def is_digit(code: int) -> bool:
    return 0x0030 <= code <= 0x0039  # <DIGIT>


def is_coefficient_start(code: int) -> bool:
    return is_digit(code) or code == 0x002E  # <DIGIT> | `.`


def is_letter(code: int) -> bool:
    return (
        0x0061 <= code <= 0x007A or 0x0041 <= code <= 0x005A
    )  # <LOWERCASE_LETTER> | <UPPERCASE_LETTER>


def is_variable_start(code: int) -> bool:
    return is_letter(code) or code == 0x005F  # <LETTER> | `_`


def is_printable(code: int) -> bool:
    return 0x0020 <= code <= 0x007E  # <ASCII>


def print_char_code(code: int | None) -> None:
    if code is None:  # <EOF>
        return TokenKind.EOF.value

    return chr(code) if is_printable(code) else f"U+{code:04X}"


__all__ = (
    "is_digit",
    "is_letter",
    "is_coefficient_start",
    "is_variable_start",
    "is_printable",
    "print_char_code",
)
