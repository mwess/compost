import inspect
import warnings


class NotImplementedException(Exception):
    pass


def not_implemented(obj):

    def wrapper():
        if inspect.isfunction(obj):
            typename = "Function "
        elif inspect.isclass(obj):
            typename = "Class "
        else:
            typename = ""
        raise NotImplementedException("%s%s is not implemented." % (typename, obj.__name__))

    return wrapper()


def deprecated(obj):

    def wrapper():
        warnings.filterwarnings(action="once")
        warnings.warn("%s is deprecated." % obj.__name__, DeprecationWarning)
        return obj()

    return wrapper()

