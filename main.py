import inspect
import collections.abc


class InvalidContract(Exception):
    pass


def handle_invalid_contract(var, value, conditions):
    raise InvalidContract('{var}: {value} , {conditions}'.format(var=var,
                                                                 value=value,
                                                                 conditions=conditions))


def check_contracts(contract):
    """
    :param contract: Mapping object between variable definitions and expected conditions.
    variable definition must be defined.
    conditions must be callable objects.
    """
    def decorator_v(funky):
        def handle(*args, **kwargs):
            params = inspect.signature(funky).bind(*args, **kwargs)
            params.apply_defaults()
            params = params.arguments
            for var, conditions in contract.items():
                if isinstance(conditions, collections.abc.Iterable):
                    if not all([condition(params[var]) for condition in conditions]):
                        handle_invalid_contract(var=var, value=params[var], conditions=conditions)
                else:
                    if not conditions(params[var]):
                        handle_invalid_contract(var=var, value=params[var], conditions=conditions)
            return funky(*args, **kwargs)

        return handle

    return decorator_v

# check positional
# check positional with keyword calls
# check positional with multi-args
# check positional with keyword calls and multi-contract
#
# check positional and keywords
# check positional and keywords with keyword calls
# check positional and keywords with multi-args
# check positional and keywords with keyword calls and multi-contract
#
# check with *args
# check with **kwargs
# check with user types
# check with base types
# check with python functions
# check with partials
#
# check runtime with large arrays / numpy arrays
# check runtime for small args
# check runtime for strings
