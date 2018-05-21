from functools import wraps
from pathlib import Path
import inspect
import pickle
import base64
import hashlib
import types
import os

ANNOTATE_PROGRESS = True

def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
    if inspect.isfunction(meth):
        return getattr(inspect.getmodule(meth),
                       meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
    return None

def annotateProgress(func, className=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cn = get_class_that_defined_method(func).__name__ if not className else className
        if ANNOTATE_PROGRESS:
            print(">", cn+"."+func.__name__)
        result = func(*args, **kwargs)
        if ANNOTATE_PROGRESS:
            print("<", cn+"."+func.__name__)
        return result
    return wrapper

CACHE_DISABLED = False
CACHE_DIR = os.path.dirname(os.path.abspath(__file__))+'/../cache/'
MEMORY_CACHE_AGE_LIMIT = 21

memoryCache = {}
memoryCacheAge = {}

def cached(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CACHE_DISABLED:
            return func(*args, **kwargs)

        global memoryCache
        global memoryCacheAge

        cls = get_class_that_defined_method(func)

        def pickleOrEmpty(struct):
            if type(struct) is types.FunctionType:
                source = inspect.getsource(struct).encode('utf-8')
                context = [pickleOrEmpty(g) for name, g in struct.__globals__.items() if name in struct.__code__.co_names]
                return pickleOrEmpty(source) + pickleOrEmpty(context)
            if type(struct) is types.ModuleType:
                return struct.__name__.encode("utf-8")
            try:
                return pickle.dumps(struct)
            except pickle.PickleError:
                return b"";
            except AttributeError:
                return b"";

        theSelf = args[0]
        theSelf = [pickleOrEmpty(getattr(theSelf, attr)) for attr in dir(theSelf) if attr[0:2] != '__' and not isinstance(getattr(theSelf, attr), types.MethodType)] #HACK we are ignoring all atributes and methods starting with "__*
        md5 = hashlib.md5()
        for p in theSelf:
            md5.update(p)
        theSelf = md5.digest()

        theAttr = list(args[1:]) + list(kwargs.values())
        theAttr = [pickleOrEmpty(attr) for attr in theAttr]
        md5 = hashlib.md5()
        for p in theAttr:
            md5.update(p)
        theAttr = md5.digest()

        theClass = inspect.getsourcelines(cls)[0]
        theClass = hashlib.md5(("".join(theClass)).encode('ascii')).digest()

        def baseN(num, b = 62, numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

        theSelf = baseN(int.from_bytes(theSelf, 'big'))
        theAttr = baseN(int.from_bytes(theAttr, 'big'))
        theClass = baseN(int.from_bytes(theClass, 'big'))

        key = cls.__name__+"."+func.__name__+"."+theClass+"."+theSelf+"."+theAttr
        path = CACHE_DIR+key+'.cache'

        if key in memoryCache:
            return memoryCache[key]

        if Path(path).is_file():
            with open(path, "rb") as cacheFile:
                result = pickle.load(cacheFile)
                memoryCache[key] = result
                return result

        result = func(*args, **kwargs)

        pickle.dump(result, open(path, "wb"))
        memoryCache[key] = result
        memoryCacheAge[key] = 0

        for k, v in memoryCacheAge.items():
            memoryCacheAge[k] = v+1
        memoryCacheAge = {k : v for k, v in memoryCacheAge.items() if v < MEMORY_CACHE_AGE_LIMIT}

        return result
    return wrapper
