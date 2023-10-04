"""This module contains functions to check if a code is a character of
a specific kind.
"""
from .token import TokenKind


def is_digit(code: int) -> bool:
    """Check if code is a digit.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is a digit, False otherwise.
    """
    return 0x0030 <= code <= 0x0039  # <digit>


def is_coefficient_start(code: int) -> bool:
    """Check if code is a coefficient start.

    The Coefficient can start with a digit or a dot.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is a Coefficient start, False otherwise.
    """
    return is_digit(code) or code == 0x002E  # <digit> | `.`


def is_lower_alpha(code: int) -> bool:
    """Check if code is a lowercased alpha.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is a lowercased alpha, False otherwise.
    """
    return 0x0061 <= code <= 0x007A  # <lower_alpha>


def is_upper_alpha(code: int) -> bool:
    """Check if code is an uppercased alpha.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is an uppercased alpha, False otherwise.
    """
    return 0x0041 <= code <= 0x005A  # <upper_alpha>


def is_alpha(code: int) -> bool:
    """Check if code is an alpha.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is an alpha, False otherwise.
    """
    return is_lower_alpha(code) or is_upper_alpha(code)  # <alpha>


def is_variable_start(code: int) -> bool:
    """Check if code is a variable start.

    The Variable can start with an alpha or an underscore.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is a Variable start, False otherwise.
    """
    return is_alpha(code) or code == 0x005F  # <alpha> | `_`


def is_variable_continue(code: int) -> bool:
    """Check if code is a variable continue.

    The Variable can continue with an alpha, an underscore or a digit.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is a Variable continue, False otherwise.
    """
    return is_variable_start(code) or is_digit(code)  # <alpha> | `_` | <digit>


def is_ascii(code: int) -> bool:
    """Check if code is an ASCII.

    Args:
        code (int): Unicode code point.

    Returns:
        bool: True if code is an ASCII, False otherwise.
    """
    return 0x0020 <= code <= 0x007E  # <ASCII>


def print_code(code: int | None) -> str:
    """Print code as a character or a Unicode code point.

    Args:
        code (int | None): Unicode code point. None for EOF.

    Returns:
        str: Character or Unicode code point.
    """
    if code is None:  # <EOF>
        return TokenKind.EOF.value

    return chr(code) if is_ascii(code) else f"U+{code:04X}"


__all__ = (
    "is_digit",
    "is_coefficient_start",
    "is_lower_alpha",
    "is_upper_alpha",
    "is_alpha",
    "is_variable_start",
    "is_variable_continue",
    "is_ascii",
    "print_code",
)
