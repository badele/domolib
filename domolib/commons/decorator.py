from functools import wraps

def command(funct):
    @wraps(funct)
    def _decorator(*args, **kwargs):
        return funct(*args, **kwargs)

    # Add domolib_decorated filed in decorated function
    _decorator.domolib_decorated = True
    return _decorator