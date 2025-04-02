#######################################
# IMPORTS
#######################################

from components.ERRORS   import RuntimeError
from components.RUNTIME_RESULT import RuntimeResult
from components.POSITION import Position
from components.CONTEXT import Context
from components.SYMBOL_TABLE import SymbolTable

#######################################
# COMPONENTS - VALUES - VALUE
#######################################
class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start:Position = None, pos_end:Position = None):
        self.pos_start = pos_start
        self.pos_end   = pos_end
        return self

    def set_context(self, context:Context = None):
        self.context   = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)
    
    def multiplied_by(self, other):
        return None, self.illegal_operation(other)
        
    def divided_by(self, other):
        return None, self.illegal_operation(other)
            
    def remainder_by(self, other):
        return None, self.illegal_operation(other)

    def powered_by(self , other):
        return None, self.illegal_operation(other)
    
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)
    
    def anded_by(self, other):
        return None, self.illegal_operation(other)
    
    def ored_by(self, other):
        return None, self.illegal_operation(other)
    
    def notted(self):
        return None, self.illegal_operation()
            
    def execute(self, args):
        return None, self.illegal_operation()
    
    def copy(self):
        return Exception("No method defined")
    
    def is_true(self):
        return False

    def illegal_operation(self, other = None):
        if not other: other = self
        return RuntimeError(
            self.pos_start, other.pos_end,
            "Illegal operations",
            self.context
        )