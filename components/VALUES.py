#######################################
# IMPORTS
#######################################

from components.ERRORS   import RuntimeError
from components.POSITION import Position
from components.CONTEXT import Context

#######################################
# VALUES
#######################################

class Number:
    def __init__(self, value):
        self.value = value
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
        if isinstance(other, Number):
            return (
                Number(self.value + other.value)
                .set_context(self.context),
                None
            )

    def subbed_by(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value - other.value)
                .set_context(self.context),
                None
            )
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return (
                Number(self.value * other.value)
                .set_context(self.context),
                None
            )
        
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return (
                Number(self.value / other.value)
                .set_context(self.context),
                None
            )
            
    def remainder_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return (
                Number(self.value % other.value)
                .set_context(self.context),
                None
            )

    def powered_by(self , other):
        if isinstance(other, Number):
            return (
                Number(self.value ** other.value)
                .set_context(self.context),
                None
            )
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value == other.value))
                .set_context(self.context),
                None
            )
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value != other.value))
                .set_context(self.context),
                None
            )
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value < other.value))
                .set_context(self.context),
                None
            )
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value > other.value))
                .set_context(self.context),
                None
            )
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value <= other.value))
                .set_context(self.context),
                None
            )
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value >= other.value))
                .set_context(self.context),
                None
            )
    def anded_by(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value and other.value))
                .set_context(self.context),
                None
            )
    def ored_by(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value or other.value))
                .set_context(self.context),
                None
            )
    def notted(self):
        return (
            Number(1 if self.value == 0 else 0)
            .set_context(self.context),
            None
        )
            
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)