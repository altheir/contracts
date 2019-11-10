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


@check_contracts({'args': lambda x: not x,
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


@check_contracts({'a': lambda a: a is not None,
                  'c': lambda c: c < 0,
                  'kwargs': [lambda x: x,
                             lambda x: all(item > 5 for item in x.values())]})
def positional_with_kwargs(a, b, *args, c, **kwargs):
    print(a, b, args, c, kwargs)


def test_positional_with_kwargs():
    positional_with_kwargs(5, 6, c=-1, d=7)


def test_positional_with_kwargs_failing():
    with pytest.raises(Exception):
        positional_with_kwargs(5, 6, c=-1, d=4)


@check_contracts({'a': lambda a: a > 4,
                  'b': lambda b: b > 10})
def keywords_only(*, a, b=7):
    print(a, b)


def test_keywords_only():
    keywords_only(a=5, b=11)
    with pytest.raises(Exception):
        keywords_only(a=1, b=12)


def test_invalid_default():
    with pytest.raises(Exception):
        keywords_only(a=7)


class UserT:
    @check_contracts({'a': lambda a: a > 7})
    def __init__(self, a):
        self.a = a

    @check_contracts({'args': lambda x: all(item > 7 for item in x),
                      'kwargs': lambda p: all(item < 0 for item in p.values())})
    def __call__(self, *args, **kwargs):
        print('called')

    @check_contracts({'b': lambda a: a > 7})
    def foo(self, b):
        return self.a + b


def test_user_type_constuctor():
    valid = UserT(10)
    with pytest.raises(Exception):
        invalid = UserT(5)


def test_user_type_member():
    valid = UserT(10)
    assert valid.foo(10) == 20
    with pytest.raises(Exception):
        valid = UserT(10)
        invalid_call = valid.foo(0)


def test_user_type_call():
    valid = UserT(10)
    valid(10, 11, 12, a=-1, b=-7, c=-10)
    with pytest.raises(Exception):
        valid(1, 2, 3)
    with pytest.raises(Exception):
        valid(10, 11, 12, a=1, b=2)


# todo
# check runtime with large arrays / numpy arrays
# check runtime for small args
# check runtime for strings
