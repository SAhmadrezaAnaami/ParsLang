#######################################
# IMPORTS
#######################################

from components.ERRORS import (
	IllegalCharError,
	ExpectedCharError
)

from components.POSITION import Position 
from components.TOKENS import *
from components.CONSTANTS import *
from utils.persianDigit2English import Persian2English
from utils.makeToken import makeToken
from utils.mapPersian2EnglishAlphabet import mapPersian2EnglishAlphabet


#######################################
# LEXER
#######################################

class Lexer:
	def __init__(self, file_name:str, text:str):
		self.fn 		  = file_name
		self.text 		  = text
		self.pos  		  = Position(-1, 0, -1, file_name, text)
		self.current_char = None
		self.advance()
	
	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

	def make_tokens(self):
		tokens = []
		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char == "#":
				self.skip_comment()
			elif self.current_char in LETTERS+NONENGLISH_LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char in DIGITS+NONENGLISH_DIGITS:
				tokens.append(self.make_number())
			elif self.current_char == '"':
				tokens.append(self.make_string())
			elif self.current_char in ";\n":
				tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
				self.advance()
			elif self.current_char in "+()*%^/,[]":
				tokens.append(makeToken(self.current_char,self.pos))
				self.advance()
			elif self.current_char == "!":
				tok, error = self.make_not_equal()
				if error: return [], error
				tokens.append(tok)
			elif self.current_char == "=":
				tokens.append(self.make_equals())
			elif self.current_char == "<":
				tokens.append(self.make_less_than())
			elif self.current_char == ">":
				tokens.append(self.make_grater_than())
			elif self.current_char == "-":
				tokens.append(self.make_minus_or_arrow())
			else:
				pos_start = self.pos.copy()
				char 	  = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		tokens.append(Token(TT_EOF, pos_start=self.pos))
		return tokens, None

	def make_number(self):
		num_str   = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS+NONENGLISH_DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
				num_str += '.'
			else:
				num_str += Persian2English(self.current_char)
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

	def make_identifier(self):
		id_str 		= ''
		real_id_str = ''
		pos_start 	= self.pos.copy()
  
		while self.current_char != None and self.current_char in LETTERS_DIGITS + NONENGLISH_LETTERS + "_":
			real_id_str = real_id_str + self.current_char
			id_str = id_str + mapPersian2EnglishAlphabet(self.current_char)
			self.advance()
   
		if real_id_str in NONENGLISH_MAP.keys():
			id_str = NONENGLISH_MAP[real_id_str]
			tok_type = TT_KEYWORD
		else :
			tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER

		return Token(tok_type, id_str, pos_start, self.pos)

	def make_not_equal(self):
		pos_start = self.pos.copy()
		self.advance()
  
		if self.current_char == '=':
			self.advance()
			return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None


		self.advance()
		return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

	def make_equals(self):
		tt_type = TT_EQ
		pos_start = self.pos.copy()
		self.advance()
		if self.current_char == "=":
			self.advance()
			tt_type = TT_EE
   
		return Token(tt_type, pos_start=pos_start, pos_end=self.pos)

	def make_less_than(self):
		tt_type = TT_LT
		pos_start = self.pos.copy()
		self.advance()
		if self.current_char == "=":
			self.advance()
			tt_type = TT_LTE
   
		return Token(tt_type, pos_start=pos_start, pos_end=self.pos)

	def make_grater_than(self):
		tt_type = TT_GT
		pos_start = self.pos.copy()
		self.advance()
		if self.current_char == "=":
			self.advance()
			tt_type = TT_GTE
   
		return Token(tt_type, pos_start=pos_start, pos_end=self.pos)

	def make_minus_or_arrow(self):
		tok_type = TT_MINUS
		pos_start = self.pos.copy()
		self.advance()
  
		if self.current_char == ">":
			self.advance()
			tok_type = TT_ARROW
   
		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_string(self):
		string = ''
		pos_start = self.pos.copy()
		escape_character = False
		self.advance()
  
		escape_characters = {
			'n' : '\n',
			't' : '\t'
		}

		while self.current_char != None and (self.current_char != '"' or escape_character):
			if escape_character :
				string += escape_characters.get(
					self.current_char, self.current_char
				)
				escape_character = False
			else:
				if self.current_char == '\\':
					escape_character = True
				else:
					string += self.current_char
			self.advance()
   
		self.advance()
		return Token(TT_STRING, string, pos_start, self.pos)

	def skip_comment(self):
		self.advance()
		while self.current_char != '\n':
			self.advance()
		self.advance()