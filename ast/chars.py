from .token import TokenKind


def is_digit(code: int) -> bool:
    return 0x0030 <= code <= 0x0039  # <digit>


def is_coefficient_start(code: int) -> bool:
    return is_digit(code) or code == 0x002E  # <digit> | `.`


def is_lower_alpha(code: int) -> bool:
    return 0x0061 <= code <= 0x007A  # <lower_alpha>


def is_upper_alpha(code: int) -> bool:
    return 0x0041 <= code <= 0x005A  # <upper_alpha>


def is_alpha(code: int) -> bool:
    return is_lower_alpha(code) or is_upper_alpha(code)  # <alpha>


def is_variable_start(code: int) -> bool:
    return is_alpha(code) or code == 0x005F  # <alpha> | `_`


def is_printable(code: int) -> bool:
    return 0x0020 <= code <= 0x007E  # <ASCII>


def print_code(code: int | None) -> None:
    if code is None:  # <EOF>
        return TokenKind.EOF.value

    return chr(code) if is_printable(code) else f"U+{code:04X}"


__all__ = (
    "is_digit",
    "is_coefficient_start",
    "is_lower_alpha",
    "is_upper_alpha",
    "is_alpha",
    "is_variable_start",
    "is_printable",
    "print_code",
)
