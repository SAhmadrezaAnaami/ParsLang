#######################################
# IMPORTS
#######################################

from components.TOKENS import *
from components.NODES import *
from components.VALUES.NUMBER import Number
from components.VALUES.STRING import String
from components.VALUES.BASE_FUNCTION import BaseFunction
from components.VALUES.LIST import List
from components.CONTEXT import Context
from components.RUNTIME_RESULT import RuntimeResult
from components.ERRORS import RuntimeError
import os

#######################################
# BUILT-IN FUNCTION
#######################################

class BuiltinFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RuntimeResult()
		exec_context = self.generate_new_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)
	
		res.register(
			self.check_and_populate_args(method.arg_names, args, exec_context)
		)
		if res.should_return(): return res
  
		return_value = res.register(
			method(exec_context)
		)
		if res.should_return(): return res
  
		return res.success(
			return_value
		)
  
	def no_visit_method(self, node, context):
		raise Exception(f"no execute_{self.name} method defined")
  
	def copy(self):
		copy = BuiltinFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<Built-in Function {self.name}>"

	###################### / Builtin Functions / ###########################
 
	def execute_print(self, exec_context:Context):
		print(
			str(exec_context.symbol_table.get('value'))
		)
		return RuntimeResult().success(Number.NULL)
	execute_print.arg_names = ["value"]


	def execute_print_ret(self, exec_context:Context):
		return RuntimeResult().success(
			String(
				str(exec_context.symbol_table.get('value'))
			)
		)
	execute_print_ret.arg_names = ["value"]

	def execute_input(self, exec_context:Context):
		text = input()
		return RuntimeResult().success(String(text))
	execute_input.arg_names = []

	def execute_input_int(self, exec_context:Context):
		while True:
			text = input()
			try:
				text = int(text)
				break
			except:
				print(f"'{text}' must be integer. try again!")
		return RuntimeResult().success(Number(text))
	execute_input_int.arg_names = []
 
	def execute_clear(self, exec_context:Context):
		os.system('cls' if os.name == "nt" else 'clear')
		return RuntimeResult().success(Number.NULL)
	execute_clear.arg_names = []
 
	def execute_is_number(self, exec_context:Context):
		is_number = isinstance(
			exec_context.symbol_table.get('value'),
			Number
		)
		return RuntimeResult().success(
			Number.TRUE if is_number else Number.FALSE
		)
	execute_is_number.arg_names = ['value'] 
	
	def execute_is_string(self, exec_context:Context):
		is_number = isinstance(
			exec_context.symbol_table.get('value'),
			String
		)
		return RuntimeResult().success(
			Number.TRUE if is_number else Number.FALSE
		)
	execute_is_string.arg_names = ['value'] 
	
	def execute_is_list(self, exec_context:Context):
		is_number = isinstance(
			exec_context.symbol_table.get('value'),
			List
		)
		return RuntimeResult().success(
			Number.TRUE if is_number else Number.FALSE
		)
	execute_is_list.arg_names = ['value'] 
	
	def execute_is_function(self, exec_context:Context):
		is_number = isinstance(
			exec_context.symbol_table.get('value'),
			BaseFunction
		)
		return RuntimeResult().success(
			Number.TRUE if is_number else Number.FALSE
		)
	execute_is_function.arg_names = ['value'] 
	
	def execute_append(self, exec_context:Context):
		list_ = exec_context.symbol_table.get('list'),
		value = exec_context.symbol_table.get('value'),
		
		if not isinstance(list_, List):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"First argument must be a list.",
					exec_context
				)
			)
   
		list_.elements.append(value)
  
		return RuntimeResult().success(Number.NULL)
	execute_append.arg_names = ['list', 'value'] 
	
	def execute_pop(self, exec_context:Context):
		list_ = exec_context.symbol_table.get('list'),
		index = exec_context.symbol_table.get('value'),
		
		if not isinstance(list_, List):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"First argument must be a list.",
					exec_context
				)
			)
		if not isinstance(index, Number):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"Second argument must be an index number.",
					exec_context
				)
			)

		try:
			element = list_.elements.pop(index.value)
		except:
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"Out of range index.",
					exec_context
				)
			)
  
		return RuntimeResult().success(element)
	execute_pop.arg_names = ['list', 'index'] 
	
	def execute_extend(self, exec_context:Context):
		list1 = exec_context.symbol_table.get('list1'),
		list2 = exec_context.symbol_table.get('list2'),
		
		if not isinstance(list1, List):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"First argument must be a list.",
					exec_context
				)
			)
		if not isinstance(list2, List):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"Second argument must be a list too idiot",
					exec_context
				)
			)

		list1.elements.extend(list2.elements)  
		return RuntimeResult().success(Number.NULL)

	execute_extend.arg_names = ['list1', 'list2']
 


	def execute_len(self, exec_context:Context):
		list_ = exec_context.symbol_table.get('list')

		if not isinstance(list_, List):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"Argument must be a list.",
					exec_context
				)
			)

		return RuntimeResult().success(
			Number(len(list_.elements))
		)
	execute_len.arg_names = ['list']

	def execute_run(self, exec_context:Context):
		fn = exec_context.symbol_table.get('fn')

		if not isinstance(fn, String):
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					"Argument must be a string.",
					exec_context
				)
			)

		fn = fn.value

		try:
			with open(fn, 'r') as f:
				script = f.read()
		except Exception as e:
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					f"Failed to load script \"{fn}\"\n" + str(e),
					exec_context
				)
			)

		_, error = run(fn, script)

		if error:
			return RuntimeResult().failure(
				RuntimeError(
					self.pos_start,self.pos_end,
					f"Failed to finish executing script \"{fn}\"\n" + error.as_string(),
					exec_context
				)
			)

		return RuntimeResult().success(Number.NULL)

	execute_run.arg_names = ['fn']


BuiltinFunction.print           = BuiltinFunction("print")
BuiltinFunction.print_ret       = BuiltinFunction("print_ret")
BuiltinFunction.input           = BuiltinFunction("input")
BuiltinFunction.input_int       = BuiltinFunction("input_int")
BuiltinFunction.clear           = BuiltinFunction("clear")
BuiltinFunction.is_number       = BuiltinFunction("is_number")
BuiltinFunction.is_string       = BuiltinFunction("is_string")
BuiltinFunction.is_list         = BuiltinFunction("is_list")
BuiltinFunction.is_function     = BuiltinFunction("is_function")
BuiltinFunction.append          = BuiltinFunction("append")
BuiltinFunction.pop             = BuiltinFunction("pop")
BuiltinFunction.extend          = BuiltinFunction("extend")
BuiltinFunction.len				= BuiltinFunction("len")
BuiltinFunction.run             = BuiltinFunction("run")

#######################################
# IMPORTS
#######################################

from components.LEXER import Lexer
from components.PARSER import Parser 
from components.INTERPRETER import Interpreter
from components.SYMBOL_TABLE import SymbolTable
from components.CONSTANTS import *


#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()

statement_mapping = {
    tuple(TRUE_STATEMENTS)						: Number.TRUE,
    tuple(FALSE_STATEMENTS + NULL_STATEMENTS)	: Number.FALSE,
    tuple(PRINT_STATEMENTS)						: BuiltinFunction.print,
    tuple(PRINT_RET_STATEMENTS)					: BuiltinFunction.print_ret,
    tuple(INPUT_STATEMENTS)						: BuiltinFunction.input,
    tuple(INPUT_INT_STATEMENTS)					: BuiltinFunction.input_int,
    tuple(CLEAR_STATEMENTS)						: BuiltinFunction.clear,
    tuple(IS_NUMBER_STATEMENTS)					: BuiltinFunction.is_number,
    tuple(IS_STRING_STATEMENTS)					: BuiltinFunction.is_string,
    tuple(IS_LIST_STATEMENTS)					: BuiltinFunction.is_list,
    tuple(IS_FUNCTION_STATEMENTS)				: BuiltinFunction.is_function,
    tuple(APPEND_STATEMENTS)					: BuiltinFunction.append,
    tuple(EXTEND_STATEMENTS)					: BuiltinFunction.extend,
    tuple(POP_STATEMENTS)						: BuiltinFunction.pop,
    tuple(LEN_STATEMENTS)						: BuiltinFunction.len,
    tuple(RUN_STATEMENTS)						: BuiltinFunction.run,
}

for statements, value in statement_mapping.items():
    for statement in statements:
        global_symbol_table.set(statement, value)

def run(fn, text):
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error
	
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error