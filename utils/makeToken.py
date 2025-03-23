from components.TOKENS import *
from components.POSITION import Position

def makeToken(current_char:str , pos:Position):
    """
    Creates a Token object based on the given character and its position.

    This function checks the provided character against several arithmetic and punctuation
    symbols and instantiates the corresponding token with the starting position set to 'pos'.
    The token type corresponds to the symbol identified by 'current_char'.

    Parameters:
        current_char (str): The character to be tokenized.
        pos (Position): The position information associated with the character.

    Returns:
        Token: An instance of the Token class corresponding to the provided character.
    """
    if current_char == '+':
        t = Token(TT_PLUS, pos_start=pos)
    elif current_char == '-':
        t = Token(TT_MINUS, pos_start=pos)
    elif current_char == '*':
        t = Token(TT_MUL, pos_start=pos)
    elif current_char == '/':
        t = Token(TT_DIV, pos_start=pos)
    elif current_char == '%':
        t = Token(TT_REMAIN, pos_start=pos)
    elif current_char == '^':
        t = Token(TT_POW, pos_start=pos)
    elif current_char == '(':
        t = Token(TT_LPAREN, pos_start=pos)
    elif current_char == ')':
        t = Token(TT_RPAREN, pos_start=pos)
    elif current_char == '=':
        t = Token(TT_EQ, pos_start=pos)
    
    
    
    return t


## actual code in LEXER file

# elif self.current_char == '+':
# 	tokens.append(Token(TT_PLUS, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == '-':
# 	tokens.append(Token(TT_MINUS, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == '*':
# 	tokens.append(Token(TT_MUL, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == '/':
# 	tokens.append(Token(TT_DIV, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == '%':
# 	tokens.append(Token(TT_REMAIN, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == '^':
# 	tokens.append(Token(TT_POW, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == '(':
# 	tokens.append(Token(TT_LPAREN, pos_start=self.pos))
# 	self.advance()
# elif self.current_char == ')':
# 	tokens.append(Token(TT_RPAREN, pos_start=self.pos))
# 	self.advance()