#######################################
# IMPORTS
#######################################

from components.VALUES.VALUE import Value
from components.VALUES.NUMBER import Number

#######################################
# COMPONENTS - VALUES - STRING
#######################################

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def added_to(self, other):
        if isinstance(other, String):
            return String(
                self.value + other.value
            ).set_context(
                self.context
            ), None
        elif isinstance(other, Number):
            return String(
                self.value + str(other.value)
            ).set_context(
                self.context
            ), None
        else :
            return None, Value.illegal_operation(self, other)
        
    def subbed_by(self, other):
        if isinstance(other, String):
            return String(
                self.value.replace(other.value, '')
            ).set_context(
                self.context
            ), None

        elif isinstance(other, Number):
            return String(
                self.value.replace(str(other.value), '')
            ).set_context(
                self.context
            ), None
        else :
            return None, Value.illegal_operation(self, other)
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return String(
                self.value * other.value
            ).set_context(
                self.context
            ), None
        else :
            return None, Value.illegal_operation(self, other)
        
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return self.value
    def __repr__(self):
        return f'"{self.value}"'