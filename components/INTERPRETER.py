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

#######################################
# INTERPRETER
#######################################

class Interpreter:
	def visit(self, node : NumberNode|UnaryOpNode|BinOpNode|VarAccessNode|VarAssignNode , context: Context) -> RuntimeResult:
		#visit_BinOpNode
		#visit_NumberNode
		#visit_UnaryOpNode
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name , self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context:Context):
		raise Exception(f"no visit_{type(node).__name__} method defined")

	def visit_VarAccessNode(self, node: VarAccessNode, context:Context):
		res 	 = RuntimeResult()
		var_name = node.var_name_tok.value
		value 	 = context.symbol_table.get(var_name)
  
		if not value:
			return res.failure(RuntimeError(
				node.pos_start, node.pos_end,
				f"'{var_name}' is not defined",
				context
			))

		value = value.copy().set_pos(
			node.pos_start, node.pos_end
		).set_context(
			context
		)
		return res.success(value)

	def visit_VarAssignNode(self, node:VarAssignNode, context:Context):
		res = RuntimeResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node , context))
		if res.should_return(): return res

		context.symbol_table.set(var_name, value)
		return res.success(value)


	def visit_ListNode(self, node:ListNode, context:Context):
		res = RuntimeResult()
		elements = []
  
		for element_node in node.element_nodes:
			elements.append(res.register(
				self.visit(element_node, context)
			))
			if res.should_return(): return res
   
		return res.success(
			List(elements).set_context(
				context
			).set_pos(
				node.pos_start,
				node.pos_end
			)
		)
  
	def visit_NumberNode(self, node:NumberNode, context:Context):
		return RuntimeResult().success( 
			Number(node.tok.value)
   			.set_context(context)
      		.set_pos(node.pos_start, node.pos_end)
		)		
   
	def visit_BinOpNode(self, node:BinOpNode, context:Context):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return() : return res
		right = res.register(self.visit(node.right_node, context))
		if res.should_return() : return res
  
		if node.op_tok.type	  == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:
			result, error = left.multiplied_by(right)
		elif node.op_tok.type == TT_DIV:
			result, error = left.divided_by(right)
		elif node.op_tok.type == TT_REMAIN:
			result, error = left.remainder_by(right)
		elif node.op_tok.type == TT_POW:
			result, error = left.powered_by(right)
		elif node.op_tok.type == TT_EE:
			result, error = left.get_comparison_eq(right)
		elif node.op_tok.type == TT_NE:
			result, error = left.get_comparison_ne(right)
		elif node.op_tok.type == TT_LT:
			result, error = left.get_comparison_lt(right)
		elif node.op_tok.type == TT_GT:
			result, error = left.get_comparison_gt(right)
		elif node.op_tok.type == TT_LTE:
			result, error = left.get_comparison_lte(right)
		elif node.op_tok.type == TT_GTE:
			result, error = left.get_comparison_gte(right)
		elif node.op_tok.matches_list(TT_KEYWORD, AND_STATEMENTS):
			result, error = left.anded_by(right)
		elif node.op_tok.matches_list(TT_KEYWORD, OR_STATEMENTS):
			result, error = left.ored_by(right)

		if error:
			return res.failure(error)
		else :		
			return res.success(
				result.set_pos(node.pos_start, node.pos_end)
			)

	def visit_UnaryOpNode(self, node:UnaryOpNode, context:Context):
		res = RuntimeResult()
		number = res.register(self.visit(node.node, context))
		if res.should_return() : return res

		error = None

		if node.op_tok.type == TT_MINUS:
			number , error = number.multiplied_by(Number(-1))
		elif node.op_tok.matches_list(TT_KEYWORD, NOT_STATEMENTS):
			number, error = number.notted()


		if error :
			return res.failure(error)
		else:
			return res.success(
				number.set_pos(node.pos_start, node.pos_end)
			)
   
	def visit_ifNode(self, node, context):
		res = RuntimeResult()

		for condition , expr, should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(Number.NULL if should_return_null else expr_value)

		if node.else_case:
			expr, should_return_null = node.else_case
			else_value = res.register(
				self.visit(expr, context)
			)
			if res.should_return(): return res
			return res.success(Number.NULL if should_return_null else else_value)

		return res.success(Number.NULL)

	def visit_forNode(self, node, context):
		res = RuntimeResult()
		elements = []
  
		start_value = res.register(
			self.visit(node.start_value_node, context)
		)
		if res.should_return(): return res
		
		end_value = res.register(
			self.visit(node.end_value_node, context)
		)
		if res.should_return(): return res
		
		if node.step_value_node:
			step_value = res.register(
				self.visit(node.step_value_node, context)
			)
			if res.should_return(): return res
		else:
			step_value = Number(1)
   
		i = start_value.value
  
		if step_value.value >= 0 :
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value
   
		while condition():
			context.symbol_table.set(
				node.var_name_tok.value, Number(i)
			)
			i += step_value.value
   
			
			value = res.register(self.visit(node.body_node , context))
			
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
   
			if res.loop_should_continue:
				continue

			if res.loop_should_break:
				break

			elements.append(value)
   
		return res.success(
			Number.NULL if node.should_return_null else
			List(elements).set_context(context).set_pos(
				node.pos_start,
				node.pos_end
			)
		)

	def visit_whileNode(self, node, context):
		res = RuntimeResult()
		elements = []
	
		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			value = res.register(self.visit(node.body_nod , context))
			
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
   
			if res.loop_should_continue:
				continue

			if res.loop_should_break:
				break
   
			elements.append(value)
   
		return res.success(
			Number.NULL if node.should_return_null else
			List(elements).set_context(
				context
			).set_pos(
				node.pos_start,
				node.pos_end
			)
		)

	def visit_FuncDefNode(self, node, context):
		res = RuntimeResult()
  
		function_name = node.var_name_token.value if node.var_name_token else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
  
		func_value = Function(
			function_name,
			body_node,
			arg_names,
			node.should_auto_return
		).set_context(
			context
		).set_pos(
			node.pos_start,
			node.pos_end
		)
  
		if node.var_name_token:
			context.symbol_table.set(function_name, func_value)
  
		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RuntimeResult()
		args = []

		value_to_call = res.register(self.visit(
			node.node_to_call, context
		))
  
		if res.should_return(): return res
  
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
  
		for arg_node in node.arg_nodes:
			args.append(
				res.register(self.visit(
					arg_node, context
				))
			)
			if res.should_return(): return res
	
		return_value = res.register(value_to_call.execute(args))
		if res.should_return(): return res
  
		return_value = return_value.copy().set_pos(
			node.pos_start, node.pos_end
		).set_context(
			context
		)
  
		return res.success(return_value)

	def visit_StringNode(self, node:StringNode, context):
		return RuntimeResult().success(
			String(
				node.tok.value,
			).set_context(
				context
			).set_pos(
				node.pos_start, node.pos_end
			)
		)
  
	def visit_ReturnNode(self, node, context):
		res = RuntimeResult()

		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else:
			value = Number.NULL

		return res.success_return(value)
   
	def visit_ContinueNode(self, node, context):
		return RuntimeResult().success_continue()
		
	def visit_BreakNode(self, node, context):
		return RuntimeResult().success_break()

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return
        
	def execute(self, args):
		res = RuntimeResult()
		interpreter = Interpreter()
		exec_context = self.generate_new_context()
		
		res.register(
			self.check_and_populate_args(self.arg_names, args, exec_context)
		)
		if res.should_return(): return res
			
		value = res.register(interpreter.visit(self.body_node, exec_context))
		if res.should_return() and res.function_return_value == None: return res
		
		return_value = (value if self.should_auto_return else None) or res.function_return_value or Number.NULL
		return res.success(return_value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<Function {self.name}>"