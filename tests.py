import pytest
from main import check_contracts


def positional(a, b):
    print(a, b)


def positional_with_variable(a, b, *args):
    print(a, b, args)


def positional_and_keywords(a, b, *args, c):
    print(a, b, args, c)


def positional_with_kwargs(a, b, *args, c, **kwargs):
    print(a, b, args, c, kwargs)


def positional_with_only_kwargs(a, b, **kwargs):
    print(a, b, kwargs)


def keywords_only(*, a, b):
    print(a, b)


class UserT:
    def __init__(self, a):
        self.a = a

    def __call__(self, *args, **kwargs):
        print('called')

    def foo(self, b):
        return self.a + b



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
# check useable on user class functions

# check runtime with large arrays / numpy arrays
# check runtime for small args
# check runtime for strings
