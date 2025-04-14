from ._tokentype import TokenType

class Token:
    
    def __init__(self, value: str, type: TokenType):
        self.value = value
        self.type = type
