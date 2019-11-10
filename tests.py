import pytest
from main import check_contracts


@check_contracts({'a': [lambda x: x is not None,
                        lambda x: x > 5],
                  'b': [lambda x: isinstance(x, str)]})
def positional(a, b):
    print(a, b)

@check_contracts({'a': lambda x: x is not None,
                  'b': lambda x: isinstance(x, str)})
def positional_single_restriction(a, b):
    print(a, b)



def test_positional_expected():
    positional(7, 'foo')


def test_positional_breaking_one_condition():
    with pytest.raises(Exception):
        positional(0, 'foo')
    with pytest.raises(Exception):
        positional(None, 'foo')
    with pytest.raises(Exception):
        positional(7, 11)


def test_positional_breaking_both_conditions():
    with pytest.raises(Exception):
        positional(0, 1)


def test_positional_single_expected():
    positional_single_restriction(7, 'foo')


def test_positional_single_breaking_one_condition():
    with pytest.raises(Exception):
        positional_single_restriction(None, 'foo')
    with pytest.raises(Exception):
        positional_single_restriction(7, 11)


def test_positional_single_breaking_both_conditions():
    with pytest.raises(Exception):
        positional_single_restriction(None, 1)


def test_positional_expected_kwarg_calls():
    positional(a=7, b='foo')


def test_positional_breaking_one_condition_kwarg_calls():
    with pytest.raises(Exception):
        positional(a=0, b='foo')
    with pytest.raises(Exception):
        positional(a=None, b='foo')
    with pytest.raises(Exception):
        positional(a=7, b=11)


def test_positional_breaking_both_conditions_kwarg_calls():
    with pytest.raises(Exception):
        positional(a=0, b=1)


def test_positional_single_expected_kwarg_calls():
    positional_single_restriction(a=7, b='foo')


def test_positional_single_breaking_one_condition_kwarg_calls():
    with pytest.raises(Exception):
        positional_single_restriction(a=None, b='foo')
    with pytest.raises(Exception):
        positional_single_restriction(a=7, b=11)


def test_positional_single_breaking_both_conditions_kwarg_calls():
    with pytest.raises(Exception):
        positional_single_restriction(a=None, b=1)


def test_positional_expected_mixed_calls():
    positional(7, b='foo')


def test_positional_breaking_one_condition_mixed_calls():
    with pytest.raises(Exception):
        positional(0, b='foo')
    with pytest.raises(Exception):
        positional(None, b='foo')
    with pytest.raises(Exception):
        positional(7, b=11)


def test_positional_breaking_both_conditions_mixed_calls():
    with pytest.raises(Exception):
        positional(0, b=1)


def test_positional_single_expected_mixed_calls():
    positional_single_restriction(7, b='foo')


def test_positional_single_breaking_one_condition_mixed_calls():
    with pytest.raises(Exception):
        positional_single_restriction(None, b='foo')
    with pytest.raises(Exception):
        positional_single_restriction(7, b=11)


def test_positional_single_breaking_both_conditions_mixed_calls():
    with pytest.raises(Exception):
        positional_single_restriction(None, b=1)

@check_contracts({'a': [lambda x: x is not None,
                        lambda x: x > 5],
                  'b': lambda x: isinstance(x, str),
                  'args': lambda x: x is not None})
def positional_with_variable(a, b, *args):
    print(a, b, args)

@check_contracts({'args': lambda x: all(item > 5 for item in x)})
def positional_arg_value_query(a, b, *args):
    print(a, b, args)


def test_positional_with_variable_args_success():
    positional_with_variable(10, 'foo', (3, 4, 5, 6, 7))


def test_positional_with_variable_args_success_two():
    positional_with_variable(10, 'foo', 3, 4, 5, 6, 7)


def test_positional_with_variable_args_failure():
    positional_arg_value_query(10, 'foo', 10, 8, 9, 6, 7)
    with pytest.raises(Exception):
        positional_arg_value_query(10, 'foo', 3, 4, 5, 6, 7)


@check_contracts({'args': lambda x: not x ,
                  'c': lambda x: x > 5})
def positional_and_keywords(a, b, *args, c):
    print(a, b, args, c)


def test_positional_and_keywords_sucess():
    positional_and_keywords(1, 2, c=7)


def test_positional_and_keywords_failure():
    with pytest.raises(Exception):
        positional_and_keywords(1, 2, 3, c=7)


def test_positional_and_keywords_failure_two():
    with pytest.raises(Exception):
        positional_and_keywords(1, 2, c=2)


def test_positional_and_keywords_sucess_kwargs():
    positional_and_keywords(a=1, b=2, c=7)


def test_positional_and_keywords_failure_two():
    with pytest.raises(Exception):
        positional_and_keywords(a=1, b=2, c=2)


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
