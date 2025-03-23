#######################################
# IMPORTS
#######################################

from components.LEXER import Lexer
from components.PARSER import Parser 
from components.INTERPRETER import Interpreter
from components.CONTEXT import Context
from components.SYMBOL_TABLE import SymbolTable
from components.VALUES import Number
from components.CONSTANTS import *


#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()

for statement in TRUE_STATEMENTS:
	global_symbol_table.set(statement, Number(1))
for statement in FALSE_STATEMENTS + NULL_STATEMENTS:
	global_symbol_table.set(statement, Number(0))


def run(fn, text):
	# Generate tokens
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error
	
	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error
