#######################################
# IMPORTS
#######################################

from utils.strings_with_arrows import *
from components.POSITION       import Position
from components.CONTEXT        import Context

#######################################
# ERRORS
#######################################

class Error:
	def __init__(self, pos_start: Position, pos_end: Position, error_name, details):
		self.pos_start   = pos_start
		self.pos_end 	 = pos_end
		self.error_name  = error_name
		self.details 	 = details
	
	def as_string(self):
		result  = f'{self.error_name}: {self.details}\n'
		result += f'File {self.pos_start.file_name}, line {self.pos_start.line + 1}'
		result += '\n\n' + string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)
		return result

class IllegalCharError(Error):
	def __init__(self, pos_start:Position, pos_end:Position, details:str):
		super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start:Position, pos_end:Position, details:str=''):
		super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
    
class ExpectedCharError(Error):
	def __init__(self, pos_start:Position, pos_end:Position, details:str=''):
		super().__init__(pos_start, pos_end, 'Expected character', details)
    
class RuntimeError(Error):
	def __init__(self, pos_start:Position, pos_end:Position, details:str, context:Context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context
  
	def as_string(self):
		result = self.generate_traceBack()
		result += f'{self.error_name}: {self.details}\n'
		result += '\n\n' + string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)
		return result

	def generate_traceBack(self):
		result 	  = ''
		pos_start = self.pos_start
		context   = self.context
  
		while context:
			result    = f' File {pos_start.file_name}, line {str(pos_start.line+1)}, in {context.display_name}\n' + result
			pos_start = context.parent_entry_position
			context   = context.parent
   
		return 'TraceBack (most recent call last):\n' + result