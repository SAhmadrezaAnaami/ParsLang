#######################################
# IMPORTS
#######################################

from components.ERRORS   import RuntimeError
from components.RUNTIME_RESULT import RuntimeResult
from components.VALUES.VALUE import Value
from components.CONTEXT import Context
from components.SYMBOL_TABLE import SymbolTable

#######################################
# COMPONENTS - VALUES - BASE FUNCTION
#######################################

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or "<anonymous>"

	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RuntimeResult()
		if len(args) > len(arg_names):
			return res.failure(
				RuntimeError(
					self.pos_start, self.pos_end,
					f"{len(args) - len(arg_names)} Too many args passed into '{self.name}'",
					self.context
				)
			)
			
		if len(args) < len(arg_names):
			return res.failure(
				RuntimeError(
					self.pos_start, self.pos_end,
					f"{len(arg_names) - len(args)} Too few args passed into '{self.name}'",
					self.context
				)
			)

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value= args[i]
			
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)
		
  
	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RuntimeResult()
		res.register(self.check_args(arg_names, args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)