import enum
from typing import Any
from dataclasses import dataclass


@enum.unique
class TokenType(enum.Enum):
    # Single character tokens
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    LEFT_BRACE = enum.auto()
    RIGHT_BRACE = enum.auto()
    COMMA = enum.auto()
    DOT = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    SEMICOLON = enum.auto()
    SLASH = enum.auto()
    STAR = enum.auto()
    # One or two character enum.tokens
    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS = enum.auto()
    LESS_EQUAL = enum.auto()
    # Lienum.terals
    INDENTIFIER = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()
    # Keenum.ywords
    AND = enum.auto()
    CLASS = enum.auto()
    ELSE = enum.auto()
    TRUE = enum.auto()
    FALSE = enum.auto()
    FUN = enum.auto()
    FOR = enum.auto()
    IF = enum.auto()
    NIL = enum.auto()
    OR = enum.auto()
    PRINT = enum.auto()
    RETURN = enum.auto()
    SUPER = enum.auto()
    THIS = enum.auto()
    VAR = enum.auto()
    WHILE = enum.auto()

    EOF = enum.auto()


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"
