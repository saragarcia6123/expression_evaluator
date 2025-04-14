from typing import Any

from ._token import Token
from ._tokentype import TokenType


def _get_token_type(token: str) -> TokenType:
    try:
        value = int(token)
        return TokenType.NUMBER
    except ValueError:
        pass

    token_definitions = {
        ('.', ',', 'e'):  TokenType.NUMBER,
        ('(', ')'): TokenType.PARENTHESIS,
        ('^', '*', '/', '+', '-'): TokenType.OPERATOR
    }  
    
    for chars, token_type in token_definitions.items():
        if token in chars:
            return token_type

    return None

def _convert_num(num: str) -> float:
    if 'e' in num or 'E' in num:
        expr= f"{float(num):.1e}".replace('+', '')
        expr = expr.replace('E', 'e')
        
        base, exponent = expr.lower().split('e')
        base = float(base)
        exponent = int(exponent)
        result = base * (10 ** exponent)
        
        return result
        
    num = float(num)
    if num.is_integer():
        num = int(num)
    return num

def _tokenize(uin: str) -> list[Token]:
    tokens = []
    prev_num = ''
    
    for c in uin:
        type = _get_token_type(c)
        
        if type == None:
            raise ValueError(f'Invalid character: {c}')
        if type == TokenType.NUMBER or prev_num != '' and prev_num[-1] == 'e':
            prev_num += c
        else:
            if prev_num != '':
                num = _convert_num(prev_num)
                tokens.append(Token(value=num, type=TokenType.NUMBER))
                prev_num = ''
            tokens.append(Token(value=c, type=type))
            
    if prev_num != '':
        num = _convert_num(prev_num)
        tokens.append(Token(value=num, type=TokenType.NUMBER))
        
    return tokens

def _validate_parenthesis(tokens: list[Token]) -> bool:
    stack = []
    for token in tokens:
        if token.value == '(':
            stack.append(token.value)
        elif token.value == ')':
            if not stack or stack.pop() != '(':
                raise ValueError
    if stack:
        raise ValueError

def _convert_num(num: str) -> float:
    if 'e' in num or 'E' in num:
        expr= f"{float(num):.1e}".replace('+', '')
        expr = expr.replace('E', 'e')
        
        base, exponent = expr.lower().split('e')
        base = float(base)
        exponent = int(exponent)
        result = base * (10 ** exponent)
        
        return result
        
    num = float(num)
    if num.is_integer():
        num = int(num)
    return num

def _infix_to_postfix(tokens: list[Token]) -> list[Token]:
    la = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3} # left-associative
    ra = {'^'} # right-associative
    output = [] # Token
    operators = [] # Token

    for token in tokens:
        if token.type == TokenType.NUMBER:
            output.append(token)
        elif token.value in la:
            while (operators and operators[-1].value in la and
                  (la[operators[-1].value] > la[token.value] or
                  (la[operators[-1].value] == la[token.value] and token.value not in ra))):
                output.append(operators.pop())
            operators.append(token)
        elif token.value == '(':
            operators.append(token)
        elif token.value == ')':
            while operators and operators[-1].value != '(':
                output.append(operators.pop())
            operators.pop()
        else:
            raise ValueError(f"Unknown token: {token.value}")

    while operators:
        output.append(operators.pop())

    return output


_OPERATIONS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y if y != 0 else 'NaN',
    '^': lambda x, y: x ** y
}

def _evaluate_postfix(postfix_tokens: list[Token]) -> float:
    stack = []
    for token in postfix_tokens:
        if token.type == TokenType.NUMBER:
            stack.append(token.value)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = _OPERATIONS[token.value](operand1, operand2)
            stack.append(result)

    return stack[0]

def _evaluate_tokens(tokens: list[Any]) -> float:
    if len(tokens) == 0:
        return 0
    postfix_tokens = _infix_to_postfix(tokens)
    result = _evaluate_postfix(postfix_tokens)
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return result

