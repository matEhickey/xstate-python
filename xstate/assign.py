from typing import Callable, Optional, Dict, Any


def not_implemented():
    pass


class Assigner:
    instance = None
    actions = {}
    
    def getInstance():
        return(Assigner.instance)
        
    def __init__(
        self,
        context
    ):
        self.context = context
        Assigner.instance = self

    def __repr__(self):
        return repr({"type": self.type})

def assign(step, funcs):    
    Assigner.actions[step] = {}
    for k in funcs.keys(): Assigner.actions[step][k] = funcs[k]