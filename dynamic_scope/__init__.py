from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect

class DynamicScope(abc.Mapping):
    def __init__(self):
        self.env: Dict[str, Optional[Any]] = {}
    
    def __getitem__(self, key: str):
        # if the key is not in the dict, raise a NameError
        if key not in self.env:
            raise NameError()
        # if the key is not in scope, raise a UnboundLocalError
        if not key_in_scope(key):
            raise UnboundLocalError()
        return self.env.__getitem__(key)
    
    def __setitem__(self, key: str, value):
        return self.env.__setitem__(key, value)
    
    def __iter__(self):
        return self.env.__iter__()
    
    def __len__(self):
        return self.env.__len__()
    
    # Override to prevent NameError when using "in"
    def __contains__(self, key:str):
        return key in self.env

def get_dynamic_re() -> DynamicScope:
    stack_info = inspect.stack()
    dynamicScope = DynamicScope()
    
    for stack in stack_info[1:]:
        f = stack.frame
        f_locals = f.f_locals
        freevars = list(f.f_code.co_freevars)
        
        for f_local in f_locals.keys():
            # don't add free variables
            if(f_local not in freevars and f_local not in dynamicScope):
                dynamicScope[f_local] = f_locals[f_local]
    #issue: keeps going after correct answer
    return dynamicScope

# Checks if the given key exists in the current scope
def key_in_scope(key: str):
    for stack in inspect.stack()[1:]:
        for f_local in stack.frame.f_locals.keys():
            if(f_local == key):
                return True

    return False