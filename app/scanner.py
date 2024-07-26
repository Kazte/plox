from token import Token
from token_type import TokenType
import lox


class Scanner:
    source: str
    tokens: list[Token]
    start: int = 0
    current: int = 0
    line: int = 1

    def __init__(self, source: str):
        self.source = source
        self.tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def _scan_token(self):
        c: chr = self._advance()

        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )

            case "\n":
                self.line += 1
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case _:
                lox.error(self.line, f"Unexpected character: {c}")

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> chr:
        self.current += 1
        return self.source[self.current - 1]

    def _add_token(self, type: TokenType):
        self._add_token(type, None)

    def _add_token(self, type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _match(self, expected: chr) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True
