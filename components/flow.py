import inspect

def getParameters(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    # if defaults:
    #     args = args[len(defaults):]
    return args

class Flow:

    def __init__(self, label, parameters, *layerConstrucotrs):
        self.label = label
        self.cascades = []

        for layer_constructor in layerConstrucotrs:

            if inspect.isclass(layer_constructor):
                layer_parameters = {}
                for param in getParameters(layer_constructor):
                    if param in parameters:
                        layer_parameters[param] = parameters[param]

                new_layer = layer_constructor(self, **layer_parameters)
                self.cascades.append(new_layer)
            else:
                self.cascades.append(layer_constructor)

    def append(self, layer):
        self.cascades.append(layer)

    def lookup(self, name, untilIndex=None):
        if untilIndex is None:
            untilIndex = len(self.cascades)
        for i in range(untilIndex - 1, -1, -1):
            layer = self.cascades[i]
            if hasattr(layer, name):
                return getattr(layer, name)
        raise AttributeError("Method "+name+" is not found")

    def __str__(self):
        return self.label

    def __getattr__(self, name):
        return self.lookup(name)
