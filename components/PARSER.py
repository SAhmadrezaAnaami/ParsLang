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
		self.update_current_tok()
		return self.current_tok

	def reverse(self ,amount=1):
		self.tok_idx -= amount
		self.update_current_tok()
		return self.current_tok

	def update_current_tok(self):
		if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]

	def parse(self) -> ParseResult:
		res = self.statements()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*', '/' '^', '==', '!=', '<', '<=', '>=', '%', 'AND' or 'OR'"
			))
		return res

	def call(self):
		res = ParseResult()
		atom = res.register(self.atom())
		if res.error: return res

		if self.current_tok.type == TT_LPAREN:
			res.register_advancements()
			self.advance()
			arg_nodes = []

			if self.current_tok.type == TT_RPAREN:
				res.register_advancements()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expression()))
				if res.error : 
					return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected 'var', INT, Float, Identifier, '+', '-' or '(' ..."
				))

				while self.current_tok.type == TT_COMMA:
					res.register_advancements()
					self.advance()
					arg_nodes.append(res.register(self.expression()))
					if res.error: return res
     
				if self.current_tok.type != TT_RPAREN:
					return res.failure(
						InvalidSyntaxError(
							self.current_tok.pos_start, self.current_tok.pos_end,
							"Expected ',' or ')'"
						)
					)

				res.register_advancements()
				self.advance()

			return res.success(
				CallNode(
					atom,
					arg_nodes
				)
			)
		return res.success(atom)

	def atom(self) -> ParseResult:
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT):
			res.register_advancements()
			self.advance()
			return res.success(NumberNode(tok))

		if tok.type in (TT_STRING):
			res.register_advancements()
			self.advance()
			return res.success(StringNode(tok))

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
    
		elif tok.type == TT_LSQUARE:
			list_expr = res.register(self.list_expr())
			if res.error: return res
			return res.success(list_expr)

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

		elif tok.matches_list(TT_KEYWORD, FUN_STATEMENTS):
			while_expr = res.register(self.func_def())
			if res.error: return res
			return res.success(while_expr)

		return res.failure(InvalidSyntaxError(
			tok.pos_start, tok.pos_end,
			"Expected INT, Float, Identifier, '+', '-' '(' 'if' 'for' 'while' 'fun'"
		))

	def power(self):
		return self.binary_operation(self.call, (TT_POW, ), self.factor)

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

	def statements(self):
		res 		= ParseResult()
		statements 	= []
		pos_start  	= self.current_tok.pos_start.copy()

		while self.current_tok.type == TT_NEWLINE:
			res.register_advancements()
			self.advance()
   
		statement = res.register(self.statement())
		if res.error: return res
		statements.append(statement)

		more_statements = True

		while True:
			newline_count = 0
			while self.current_tok.type == TT_NEWLINE:
				res.register_advancements()
				self.advance()
				newline_count = newline_count + 1
			if newline_count == 0 :
				more_statements = False

			if not more_statements: break
			statement = res.try_register(self.statement())
			if not statement:
				self.reverse(res.to_reverse_count)
				more_statements = False
				continue
			statements.append(statement)
		return res.success(ListNode(
				statements	,
				pos_start	,
				self.current_tok.pos_end.copy()
			))

	def statement(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if self.current_tok.matches_list(TT_KEYWORD, RETURN_STATEMENTS):
			res.register_advancements()
			self.advance()

			expr = res.try_register(self.expression())
			if not expr:
				self.reverse(res.to_reverse_count)

			return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches_list(TT_KEYWORD, CONTINUE_STATEMENTS):
			res.register_advancements()
			self.advance()
			if self.current_tok.type == TT_NEWLINE:
				res.register_advancements()
				self.advance()
			return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches_list(TT_KEYWORD, BREAK_STATEMENTS):
			res.register_advancements()
			self.advance()
			if self.current_tok.type == TT_NEWLINE:
				res.register_advancements()
				self.advance()
			return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

		expr = res.register(self.expression())
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'return', 'continue', 'break', 'var', INT, Float, Identifier, '+', '-' '(' 'if' 'for' 'while' 'fun' "
			))

		return res.success(expr)

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
   
		ops = [(TT_KEYWORD, key) for key in AND_STATEMENTS+OR_STATEMENTS]
	
		node = res.register(
			self.binary_operation(self.comp_expr, ops)
		)
  
		if res.error : 
			return res.failure(InvalidSyntaxError(
			self.current_tok.pos_start, self.current_tok.pos_end,
			"Expected 'var', INT, Float, Identifier, '+', '-' '(' 'if' 'while' 'for' 'fun' "
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
		all_cases = res.register(self.if_expr_cases(IF_STATEMENTS))
		if res.error: return res
		cases, else_case = all_cases
		return res.success(ifNode(cases, else_case))

	def if_expr_cases(self, case_keywords):
		res = ParseResult()
		cases = []
		else_case = None
  
		if not self.current_tok.matches_list(TT_KEYWORD, case_keywords):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected either {case_keywords} statements."
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
					f"Expected either {THEN_STATEMENTS} statements."
				)
			)
			
		res.register_advancements()
		self.advance()
  
		if self.current_tok.type == TT_NEWLINE:
			res.register_advancements()
			self.advance()
			
			statements = res.register(self.statements())
			if res.error: return res
			cases.append((condition, statements, True))
  
			if self.current_tok.matches_list(TT_KEYWORD,END_STATEMENTS ):
				res.register_advancements()
				self.advance()
			else:
				all_cases = res.register(self.if_expr_b_or_c())
				if res.error: return res
				new_cases, else_case = all_cases
				cases.extend(new_cases)
		else:
			expr = res.register(self.statement())
			if res.error: return res
			cases.append((condition, expr, False))

			all_cases = res.register(self.if_expr_b_or_c())
			if res.error: return res
			new_cases, else_case = all_cases
			cases.extend(new_cases)

		return res.success(
			(cases, else_case)
		)
  
	def if_expr_b(self):
		return self.if_expr_cases(ELIF_STATEMENTS)
  
	def if_expr_c(self):
		res = ParseResult()
		else_case = None

		if self.current_tok.matches_list(TT_KEYWORD, ELSE_STATEMENTS):
			res.register_advancements()
			self.advance()

			if self.current_tok.type == TT_NEWLINE:
				res.register_advancements()
				self.advance()

				statements = res.register(self.statements())
				if res.error: return res
				else_case = (statements, True)

				if self.current_tok.matches_list(TT_KEYWORD, END_STATEMENTS):
					res.register_advancements()
					self.advance()
				else:
					return res.failure(
						InvalidSyntaxError(
							self.current_tok.pos_start, self.current_tok.pos_end,
							"Expected 'end'"
						)
					)
			else:
				expr = res.register(self.statement())
				if res.error: return res
				else_case = (expr, False)
				
			return res.success(else_case)
   
	def if_expr_b_or_c(self):
		res = ParseResult()
		cases , else_case = [], None
  
		if self.current_tok.matches_list(TT_KEYWORD, ELIF_STATEMENTS):
			all_cases = res.register(self.if_expr_b())
			if res.error: return res
			cases, else_case = all_cases
		else:
			else_case = res.register(self.if_expr_c())
			if res.error: return res
   
		return res.success(
			(cases, else_case)
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

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancements()
			self.advance()

			body = res.register(self.statements())
			if res.error: return res
			
			if not self.current_tok.matches_list(TT_KEYWORD, END_STATEMENTS):
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected 'end' statement"
					)
				)

			res.register_advancements()
			self.advance()
   
			return res.success(
				forNode(
					var_name,
					start_value,
					end_value,
					step_value,
					body,
					True
				)
			)

		body = res.register(self.statement())
		if res.error: return res
		return res.success(
			forNode(
				var_name,
				start_value,
				end_value,
				step_value,
				body,
				False
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

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancements()
			self.advance()
			
			body = res.register(self.statements())
			if res.error: return res
   
			if not self.current_tok.matches_list(TT_KEYWORD, END_STATEMENTS):
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected 'end' statement"
					)
				)

			res.register_advancements()
			self.advance()

			return res.success(
				whileNode(
					condition,
					body,
					True
				)
			)

		body = res.register(self.statement())
		if res.error: return res
		
		return res.success(
			whileNode(
				condition,
				body,
				False
			)
		)
  
	def func_def(self):
		res = ParseResult()

		if not self.current_tok.matches_list(TT_KEYWORD, FUN_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'fun' statement"
				)
			)

		res.register_advancements()
		self.advance()

		if self.current_tok.type == TT_IDENTIFIER:
			var_name_token = self.current_tok
			res.register_advancements()
			self.advance()
			
			if self.current_tok.type != TT_LPAREN:
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected '('"
					)
				)
	
		else:
			var_name_token = None
			if self.current_tok.type != TT_LPAREN:
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected IDENTIFIER or '('"
					)
				)

		res.register_advancements()
		self.advance()
		arg_name_tokens = []

		if self.current_tok.type == TT_IDENTIFIER:
			arg_name_tokens.append(self.current_tok)
			res.register_advancements()
			self.advance()
			while self.current_tok.type == TT_COMMA:
				res.register_advancements()
				self.advance()
				
				if self.current_tok.type != TT_IDENTIFIER:
					return res.failure(
						InvalidSyntaxError(
							self.current_tok.pos_start, self.current_tok.pos_end,
							f"Expected IDENTIFIER"
						)
					)

				arg_name_tokens.append(self.current_tok)
				res.register_advancements()
				self.advance()
    
			if self.current_tok.type != TT_RPAREN:
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected , or ')'"
					)
				)
		else:
			if self.current_tok.type != TT_RPAREN:
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected IDENTIFIER or ')'"
					)
				)
			
		res.register_advancements()
		self.advance()

		if self.current_tok.type == TT_ARROW:
	
			res.register_advancements()
			self.advance()

			node_to_return = res.register(self.expression())
			if res.error: return res

			return res.success(
				FuncDefNode(
					var_name_token,
					arg_name_tokens,
					node_to_return,
					True
				)
			)
  
		if self.current_tok.type != TT_NEWLINE:
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '->' or NEWLINE"
				)
			)

		res.register_advancements()
		self.advance()

		body = res.register(self.statements())
		if res.error: return res  

		if not self.current_tok.matches_list(TT_KEYWORD, END_STATEMENTS):
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected 'end' statements"
				)
			)
  
		res.register_advancements()
		self.advance()

		return res.success(
			FuncDefNode(
				var_name_token,
				arg_name_tokens,
				body,
				False
			)
		)

	def list_expr(self):
		res = ParseResult()
		element_nodes = []
		pos_start = self.current_tok.pos_start.copy()
  
		if self.current_tok.type != TT_LSQUARE:
			return res.failure(
				InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected int float + - ( '[' if for while"
				)
			)
   
		res.register_advancements()
		self.advance()
  
		if self.current_tok.type == TT_RSQUARE:
			res.register_advancements()
			self.advance()
		else:
			element_nodes.append(res.register(self.expression()))
			if res.error : 
				return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'var', INT, Float, Identifier, '+', '-' or ']' ..."
			))

			while self.current_tok.type == TT_COMMA:
				res.register_advancements()
				self.advance()
				element_nodes.append(res.register(self.expression()))
				if res.error: return res
	
			if self.current_tok.type != TT_RSQUARE:
				return res.failure(
					InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						"Expected ',' or ']'"
					)
				)

			res.register_advancements()
			self.advance()
		
		return res.success(ListNode(
			element_nodes, pos_start, self.current_tok.pos_end.copy()
		))