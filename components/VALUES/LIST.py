#######################################
# IMPORTS
#######################################

from components.ERRORS   import RuntimeError
from components.VALUES.VALUE import Value
from components.VALUES.NUMBER import Number


#######################################
# COMPONENTS - VALUES - LIST
#######################################

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
        
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None
    
    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    "Element at this index could not be removed from list because index is out of bounds",
                    self.context
                )
        else :
            return None, Value.illegal_operation(self, other)
                
    def divided_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    "Element at this index could not be retrieved from list because index is out of bounds",
                    self.context
                )
        else :
            return None, Value.illegal_operation(self, other)
        
    def multiplied_by(self, other):
        if isinstance(other , List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self,other)
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return ", ".join([str(x) for x in self.elements])
        
    
    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'