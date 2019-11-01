import inspect
import collections.abc


def check_contracts(contract):
    """
    :param contract: Mapping object between variable definitions and expected values.
    """
    def decorator_v(funky):
        def handle(*args, **kwargs):
            params = inspect.signature(funky).bind(*args, **kwargs)
            params.apply_defaults()
            params = params.arguments
            for var, conditions in contract.items():
                if isinstance(conditions, collections.abc.Iterable):
                    if not all([condition(params[var]) for condition in conditions]):
                        raise RuntimeError('Invalid contract') # todo return failed condition , Contract Runtime Error
                else:
                    if not conditions(params[var]):
                        raise RuntimeError('Invalid contract') # todo return failed condition , Contract Runtime Error
            return funky(*args, **kwargs)
        return handle
    return decorator_v


@check_contracts({'a': lambda x: x  is not None ,
                  'args':lambda x: x is not None,
                  'b': [lambda x: x<=2,lambda x:x >0]})
def funky_args(a, b, c, *args, d, e=0):
    print(a, b, c)




funky_args(1,3,3,d=4)
