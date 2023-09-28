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
        # if the key is an UnboundLocal, raise an UnboundLocalError
        if type(self.env[key]) is UnboundLocal:
            raise UnboundLocalError()
        return self.env.__getitem__(key)
    
    def __setitem__(self, key: str, value):
        return self.env.__setitem__(key, value)
    
    def __iter__(self):
        return self.env.__iter__()
    
    def __len__(self):
        return self.env.__len__()
    
    # Override to prevent NameError when using "in" keyword
    def __contains__(self, key:str):
        return key in self.env

class UnboundLocal():
    def __init__(self):
        self.error: UnboundLocalError

def get_dynamic_re() -> DynamicScope:
    dynamicScope = DynamicScope()
    # get stack information to get variables in each stack
    stack_info = inspect.stack()
    
    # skip first stack (first stack is this current function)
    for stack in stack_info[1:]:
        f = stack.frame
        f_locals = f.f_locals
        f_code = f.f_code
        freevars = list(f.f_code.co_freevars)
        allVars = list(f_code.co_varnames) + list(f_code.co_cellvars)

        for var in allVars:
            # don't add free variables and don't reassign closest local
            if(var not in freevars and var not in dynamicScope):
                value = UnboundLocal()
                if(var in f_locals):
                    value = f_locals[var]
                dynamicScope[var] = value

    return dynamicScope

def dre_first(key: str):
    return True

# Checks if the given key exists in the current scope
# def key_in_scope(key: str):
#     # skip first two stacks (first stack is this function, second is class)
#     for stack in inspect.stack()[2:]:
#         # checks if variable name is in any stack frames
#         for f_local in stack.frame.f_locals.keys():
#             if(f_local == key):
#                 return True

#     return False
# should I skip two, move this into the class, keep this here, and / or skip one