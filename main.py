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
    def decorator_v(function):
        def handle(*args, **kwargs):
            params = inspect.signature(function).bind(*args, **kwargs)
            params.apply_defaults()
            params = params.arguments
            for var, conditions in contract.items():
                if isinstance(conditions, collections.abc.Iterable):
                    if not all([condition(params[var]) for condition in conditions]):
                        handle_invalid_contract(var=var, value=params[var], conditions=conditions)
                else:
                    if not conditions(params[var]):
                        handle_invalid_contract(var=var, value=params[var], conditions=conditions)
            return function(*args, **kwargs)

        return handle

    return decorator_v
