#######################################
# IMPORTS
#######################################

from components.SYMBOL_TABLE import SymbolTable

#######################################
# CONTEXT
#######################################

class Context:
	def __init__(self, display_name:str, parent=None, parent_entry_position = None):
		self.display_name 		   		= display_name
		self.parent 			   		= parent
		self.parent_entry_position 		= parent_entry_position
		self.symbol_table:SymbolTable 	= None