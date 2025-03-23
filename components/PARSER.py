#######################################
# IMPORTS
#######################################

from components.ERRORS import (
	InvalidSyntaxError
)
from components.TOKENS import *
from components.PARSE_RESULT import ParseResult
from components.NODES import *
from components.CONSTANTS import *


#######################################
# PARSER
#######################################

class Parser:
	def __init__(self, tokens:list[Token]):
		self.tokens   = tokens
		self.tok_idx  = -1
		self.advance()

	def advance(self):
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]
		return self.current_tok

	def parse(self) -> ParseResult:
		res = self.expression()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*', '/' or '%'"
			))
		return res

	def atom(self) -> ParseResult:
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT):
			res.register_advancements()
			self.advance()
			return res.success(NumberNode(tok))

		elif tok.type == TT_IDENTIFIER:
			res.register_advancements()
			self.advance()
			return res.success(VarAccessNode(tok))

		elif tok.type == TT_LPAREN:
			res.register_advancements()
			self.advance()
			expr = res.register(self.expression())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register_advancements()
				self.advance()
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))

		elif tok.matches_list(TT_KEYWORD , IF_STATEMENTS):
			if_expr = res.register(self.if_expr())
			if res.error: return res
			return res.success(if_expr)

		elif tok.matches_list(TT_KEYWORD, FOR_STATEMENTS):
			for_expr = res.register(self.for_expr())
			if res.error: return res
			return res.success(for_expr)
      
		elif tok.matches_list(TT_KEYWORD, WHILE_STATEMENTS):
			while_expr = res.register(self.while_expr())
			if res.error: return res
			return res.success(while_expr)

		return res.failure(InvalidSyntaxError(
			tok.pos_start, tok.pos_end,
			"Expected INT, Float, Identifier, '+', '-' or '('"
		))

	def power(self):
		return self.binary_operation(self.atom, (TT_POW, ), self.factor)

	def factor(self) -> ParseResult:
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			res.register_advancements()
			self.advance()
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))
		
		return self.power()

	def term(self):
		return self.binary_operation(self.factor, (TT_MUL, TT_DIV, TT_REMAIN))

	def expression(self):
		res = ParseResult()
		if self.current_tok.matches_list(TT_KEYWORD, VAR_STATEMENTS):
			res.register_advancements()
			self.advance()
			
			if self.current_tok.type != TT_IDENTIFIER:
				res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier (provide a variable name)"
				))

			var_name = self.current_tok
			res.register_advancements()
			self.advance()
   
			if self.current_tok.type == TT_EQ:
				res.register_advancements()
				self.advance()
				expr = res.register(self.expression())
				if res.error : return res
				return res.success(VarAssignNode(var_name, expr))
			else:
				zero_tok = Token(TT_INT, 0, var_name.pos_end)
				zero_node = NumberNode(zero_tok)
				return res.success(VarAssignNode(var_name, zero_node))

			# if self.current_tok.type != TT_EQ:
			# 	res.failure(InvalidSyntaxError(
			# 		self.current_tok.pos_start, self.current_tok.pos_end,
			# 		"Expected '='"
			# 	))
    
			# res.register_advancements()
			# self.advance()
			# expr = res.register(self.expression())
			# if res.error : return res
   
			# return res.success(VarAssignNode(var_name, expr))
   
		ops = [(TT_KEYWORD, key) for key in AND_STATEMENTS+OR_STATEMENTS]
	
		node = res.register(
			self.binary_operation(self.comp_expr, ops)
		)
  
		if res.error : 
			return res.failure(InvalidSyntaxError(
			self.current_tok.pos_start, self.current_tok.pos_end,
			"Expected 'var', INT, Float, Identifier, '+', '-' or '('"
		))
  
		return res.success(node)

	def comp_expr(self):
		res = ParseResult()

		if self.current_tok.matches_list(TT_KEYWORD, NOT_STATEMENTS):
			op_token = self.current_tok
			res.register_advancements()
			self.advance()

			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(
				UnaryOpNode(op_token, node)
			)

		node = res.register(
			self.binary_operation(
       			self.arith_expr, 
				(TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)
            )
      	)
		if res.error: 
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected INT, Float, Identifier, '+', '-' or '(' 'not'"
				)
			)
		return res.success(node)

	def arith_expr(self):
		return self.binary_operation(
			self.term, (TT_PLUS,TT_MINUS)
		)

	def binary_operation(self, func_a, ops: list[str], func_b=None) -> ParseResult:
		if func_b == None:
			func_b = func_a
  
		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
			op_tok = self.current_tok
			res.register_advancements()
			self.advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)

	def if_expr(self):
		res = ParseResult()
		cases = []
		else_case = None
  
  
		if not self.current_tok.matches_list(TT_KEYWORD, IF_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected if statement"
				)
			)
   
		res.register_advancements()
		self.advance()

		condition = res.register(self.expression())
		if res.error: return res

		if not self.current_tok.matches_list(TT_KEYWORD, THEN_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected then statement"
				)
			)
			
		res.register_advancements()
		self.advance()
  
		expr = res.register(self.expression())
		if res.error: return res
		cases.append((condition, expr))

		while self.current_tok.matches_list(TT_KEYWORD, ELIF_STATEMENTS):
			res.register_advancements()
			self.advance()

			condition = res.register(self.expression())
			if res.error: return res

			if not self.current_tok.matches_list(TT_KEYWORD, THEN_STATEMENTS):
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected then statement"
					)
				)

			res.register_advancements()
			self.advance()

			expr = res.register(self.expression())
			if res.error: return res
			cases.append((condition, expr))

		if self.current_tok.matches_list(TT_KEYWORD, ELSE_STATEMENTS):
			res.register_advancements()
			self.advance()

			expr = res.register(self.expression())
			if res.error: return res
			else_case = expr
			
		return res.success(
			ifNode(cases, else_case)
		)
  
  
	def for_expr(self):
		res = ParseResult()

		if not self.current_tok.matches_list(TT_KEYWORD, FOR_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'for' statement"
				)
			)
   
		res.register_advancements()
		self.advance()

		if self.current_tok.type != TT_IDENTIFIER:
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected IDENTIFIER"
				)
			)
   
		var_name = self.current_tok
		res.register_advancements()
		self.advance()
  
		if self.current_tok.type != TT_EQ:
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '='"
				)
			)
		
		res.register_advancements()
		self.advance()
  
		start_value = res.register(self.expression())
		if res.error: return res
  
		if not self.current_tok.matches_list(TT_KEYWORD, TO_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'to' statement"
				)
			)

		res.register_advancements()
		self.advance()

		end_value = res.register(self.expression())
		if res.error: return res

		if self.current_tok.matches_list(TT_KEYWORD, STEP_STATEMENTS):
			res.register_advancements()
			self.advance()
			
			step_value = res.register(self.expression())
			if res.error: return res
		else:
			step_value = None

		if not self.current_tok.matches_list(TT_KEYWORD, THEN_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'then' statement"
				)
			)
   
		res.register_advancements()
		self.advance()

		body = res.register(self.expression())
		if res.error: return res

		return res.success(
			forNode(
				var_name,
				start_value,
				end_value,
				step_value,
				body
			)
		)


	def while_expr(self):
		res = ParseResult()
  
		if not self.current_tok.matches_list(TT_KEYWORD, WHILE_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'while' statement"
				)
			)

		res.register_advancements()
		self.advance()

		condition = res.register(self.expression())
		if res.error: return res

		if not self.current_tok.matches_list(TT_KEYWORD, THEN_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'then' statement"
				)
			)

		res.register_advancements()
		self.advance()

		body = res.register(self.expression())
		if res.error: return res
		
		return res.success(
			whileNode(
				condition,
				body
			)
		)