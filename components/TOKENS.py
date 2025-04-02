#######################################
# IMPORTS
#######################################

from components.POSITION  import Position
from components.CONSTANTS import *

#######################################
# TOKENS
#######################################

TT_INT		  	= 'INT'
TT_FLOAT      	= 'FLOAT'
TT_STRING      	= 'STRING'
TT_PLUS       	= 'PLUS'
TT_MINUS      	= 'MINUS'
TT_MUL        	= 'MUL'
TT_DIV        	= 'DIV'
TT_POW        	= 'POW'
TT_REMAIN	  	= 'REMAIN'                #remainder
TT_LPAREN     	= 'LPAREN'
TT_RPAREN     	= 'RPAREN'
TT_EOF		  	= 'EOF'
TT_IDENTIFIER 	= 'IDENTIFIER'         	# variable name
TT_KEYWORD    	= 'KEYWORD'				# VAR
TT_EQ		    = 'EQ'					# =
TT_EE		 	= "EE"
TT_NE		 	= "NE"
TT_LT			= "LT"
TT_LTE			= "LTE"
TT_GT	 		= "GT"
TT_GTE	 		= "GTE"
TT_COMMA        = "COMMA"
TT_ARROW        = "ARROW"
TT_LSQUARE      = "LSQUARE"
TT_RSQUARE      = "RSQUARE"
TT_NEWLINE      = "NEWLINE"

KEYWORDS = (
    [
    ]                   +
    RETURN_STATEMENTS   +
    CONTINUE_STATEMENTS +
    BREAK_STATEMENTS    +
    END_STATEMENTS      +
    FUN_STATEMENTS      +
    WHILE_STATEMENTS    +
    STEP_STATEMENTS     +
    TO_STATEMENTS	    +
    FOR_STATEMENTS      +
    IF_STATEMENTS       +
    ELIF_STATEMENTS     +
    ELSE_STATEMENTS     +
    THEN_STATEMENTS     +
    VAR_STATEMENTS      +
    AND_STATEMENTS      +
    OR_STATEMENTS       +
    NOT_STATEMENTS
)

class Token:
	def __init__(self, type_, value=None, pos_start:Position=None, pos_end:Position=None):
		self.type  = type_
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end   = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = pos_end
	
	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

	def matches(self, type_, value):
		return self.type == type_ and self.value == value

	def matches_list(self, type_, values):
		return self.type == type_ and self.value in values