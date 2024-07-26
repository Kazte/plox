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
            case "*":
                self._add_token(TokenType.STAR)
            case "/":
                if self._match("/"):
                    # a comment goes until the end of the line
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)

            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case '"':
                self._string()
            case "\n":
                self._add_line()
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case _:
                if self._is_digit(c):
                    self._number()
                else:
                    lox.error(self.line, f"Unexpected character: {c}")

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._add_line()
            self._advance()

        if self._is_at_end():
            lox.error(self.line, "Unterminated string.")
            return

        self._advance()

        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and self._is_digit(self._peek_next()):
            # consume the "."
            self._advance()

            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _is_digit(self, c: chr) -> bool:
        return c >= "0" and c <= "9"

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

    def _peek(self) -> chr:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> chr:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _add_line(self):
        self.line += 1
