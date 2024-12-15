from typing import Any
from src.token import Token, TokenType
from src.lox import lox
from dataclasses import dataclass, field


@dataclass
class Scanner:
    source: str
    tokens: list[Token] = field(default_factory=list)

    current: int = 0
    start: int = 0
    line: int = 1

    keywords: dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        c: str = self.advance()

        if c == "\n":
            self.line += 1
        elif c in (" ", "\r", "\t"):
            # Ignore whitespace
            pass
        elif c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)

        elif c == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                self.add_token(TokenType.SLASH_SLASH)

                # We advance until we reach the end of the line (commented line) or the end of the file
                while self.source[self.current] != "\n" and not self.is_at_end():
                    self.current += 1
            else:
                self.add_token(TokenType.SLASH)
        elif c == '"':
            self.add_string()
        elif c.isdigit():
            self.add_number()
        elif self.is_alpha(c):
            self.add_identifier()
        else:
            lox.error(self.line, f"Unexpected character: {c}")

    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or c.isdigit()

    def add_identifier(self) -> None:
        while self.is_alpha_numeric(self.source[self.current]):
            self.current += 1

        text = self.source[self.start : self.current]
        token_type = TokenType.KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def is_digit(self, c: str) -> bool:
        return c <= "9" and c >= "0"

    def add_number(self) -> None:
        """Adds number literal tokens to the token list"""
        while self.is_digit(self.source[self.current]):
            self.current += 1

        # Look for a fractional part
        if self.source[self.current] == "." and self.is_digit(
            self.source[self.current + 1]
        ):
            self.current += 1
            while self.is_digit(self.source[self.current]):
                self.current += 1

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def add_string(self) -> None:
        """Adds string literal tokens to the token list"""
        while self.source[self.current] != '"' and not self.is_at_end():
            if self.source[self.current] == "\n":
                self.line += 1
            self.current += 1

        if self.is_at_end():
            lox.error(self.line, "Unterminated string.")
            return

        self.current += 1  # Consume the closing "
        str_value = self.source[
            self.start + 1 : self.current - 1
        ]  # Trim the surrounding quotes
        self.add_token(TokenType.STRING, str_value)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
