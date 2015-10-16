# coding: utf-8

from itertools import zip_longest
from tinysegmenter import TinySegmenter


def grouper(iterable, n, fillvalue=None):
    """Group iterable into zip of n iterable"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def str_chop(string, n):
    """Chop a given string into an iterable of n strings"""
    return map(lambda itr: "".join(itr), grouper(string, n, ''))


# simple solution
def str_wrap(string, n):
    """Wrap a given string by n-char width"""
    return '\n'.join(str_chop(string, n))


str_dummy = '闕'


# desired function
def str_wrap_save_newline(string, n):
    """Wrap a given string by n-char width keeping CR"""
    iter_result = str_chop(string.replace('\n', str_dummy), n)
    return '\n'.join(map(lambda s: s.replace(str_dummy, '\n'), iter_result))


def str_wrap_with_newline(string, n, newline='\n'):
    str_list = string.split(newline)
    return newline.join(map(lambda s: str_wrap(s, n), str_list))


def apply_to_string(str_func):
    """Decorator that give a failsafe for a string function.
    str_func :: str -> A."""

    from functools import wraps

    @wraps(str_func)
    def wrapper(arg, **kwargs):
        if isinstance(arg, str):
            return str_func(arg, **kwargs)
        else:
            return arg
    return wrapper


@apply_to_string
def descape(string):
    """ASCII only"""
    return string.encode('unicode-escape').decode('utf-8')


@apply_to_string
def rescape(string):
    """ASCII only"""
    return string.encode('utf-8').decode('unicode-escape')


class GoAndReturnOperator(object):
    """Store a pair of operators to be inverse of each other."""

    def __init__(self, op_do, op_redo):
        # super(GoAndReturnOperator, self).__init__()
        self.op_do = op_do
        self.op_redo = op_redo

    def getDo(self):
        """getDo: return op_do :: A -> B."""
        return self.op_do

    def getRedo(self):
        """getRedo: return op_redo :: B -> A."""
        return self.op_redo

    def getInverse(self, operator):
        if operator == self.op_do:
            return self.op_redo
        elif operator == self.op_redo:
            return self.op_do
        else:
            raise ValueError("Invalid operator")

escape = GoAndReturnOperator(rescape, descape)


def replacer_maker(old, new):
    @apply_to_string
    def replacer(x):
        return x.replace(old, new)
    return replacer

store_newline = replacer_maker('\n', str_dummy)
restore_newline = replacer_maker(str_dummy, '\n')
newline_storer = GoAndReturnOperator(store_newline, restore_newline)


# extract and generalize modification logic as decorator pattern
def go_and_return_decorator_maker(pair):
    """Modify first with pair.op_do and revert it by pair.op_redo.

    return Decorator"""

    assert isinstance(pair, GoAndReturnOperator)

    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            # replace target in string of args
            new_args = map(pair.getDo(), args)
            result = func(*new_args, **kwargs)
            # recover target in string of output
            return pair.getRedo()(result)
        return wrapper
    return decorator

str_save = go_and_return_decorator_maker(newline_storer)
escape_dec = go_and_return_decorator_maker(escape)

# and here get the decorated function
# wrapper == str_wrap_save_newline


@escape_dec
def wrapper(string, n):
    """Wrap a given string by n-char width keeping CR"""
    return str_wrap_with_newline(string, n)


# create a string-wrapping iterator with counter
# get a iterator of string and wrapping width number
# implementation
# if given a string, token it into iterator
# pull a chunk of string from the given iterator and count its length
# if the count exceeds the wrapping width, push \n at end then keep going
# from 0 with the current string


if __name__ == '__main__':
    flavor = 20
    bio = 21
    disc = 22
    tips = 24
    n_max = 27

    n_wrap = bio
    str_input = input("Input wrapping string by {}:\n".format(n_wrap))
    result = wrapper(str_input, n_wrap)
    print(result)
