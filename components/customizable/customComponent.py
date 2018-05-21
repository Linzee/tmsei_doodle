from components.flowUtils import annotateProgress
import types

value = None
def prototypeReturnFunc(*kargs, **kwargs):
    if type(value) is types.LambdaType:
        return value(*kargs, **kwargs)
    else:
        return value

class CustomComponent:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            prototypeGlobals = dict(prototypeReturnFunc.__globals__)
            prototypeGlobals['value'] = value
            func = types.FunctionType(prototypeReturnFunc.__code__, prototypeGlobals, name=key, closure=prototypeReturnFunc.__closure__)
            func = annotateProgress(func, className=CustomComponent.__name__)
            setattr(self, key, func)
