#######################################
# SYMBOL_TABLE
#######################################

class SymbolTable:
    def __init__(self):
        self.symbols    = {}
        self.parent     = None
        
    def get(self , name:str):
        value = self.symbols.get(name, None)
        
        if value == None and self.parent:
            return self.parent.get(name)
        
        return value
    
    def set(self, name:str, value):
        self.symbols[name] = value
        
    def remove(self, name:str):
        del self.symbols[name]