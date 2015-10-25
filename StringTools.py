# coding: utf-8

from itertools import zip_longest


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


# desired function
def str_wrap_save_newline(string, n, newline='\n'):
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


class GoAndReturnOperator(object):
    """Store a pair of operators to be inverse of each other."""

    def __init__(self, op_do, op_redo):
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


def replacer_maker(old, new):
    @apply_to_string
    def replacer(x):
        return x.replace(old, new)
    return replacer

encode_newline = replacer_maker('\n', r'\n')
decode_newline = replacer_maker(r'\n', '\n')
newline_storer = GoAndReturnOperator(decode_newline, encode_newline)


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


# and here get the decorated function
# wrapper == str_wrap_save_newline
@str_save
def wrapper(string, n):
    """Wrap a given string by n-char width keeping CR"""
    return str_wrap_save_newline(string, n)


from tinysegmenter import TinySegmenter


def wrapper_jp(string, width):
    """Japanese string with newline wrapping function"""
    segmenter = TinySegmenter()
    tokens = segmenter.tokenize(string)
    token_remain = lambda: len(tokens) > 0
    # save lines shorter than width into result
    result = ""
    while token_remain():
        line = ""
        # accumulate tokens whose total is shorter than width into line
        while token_remain() and len(line + tokens[0]) <= width:
            line += tokens.pop(0)
        else:
            result += line + ('\n' if token_remain() else '')
    # print(result)
    return result


@str_save
def wrapper_jp_with_newline(string, width, newline='\n'):
    str_list = string.split(newline)
    return newline.join(map(lambda s: wrapper_jp(s, width), str_list))


if __name__ == '__main__':
    while True:
        n_wrap = int(input("Wrapping width: "))
        str_input = input("Input string to be wrapped:\n")
        result = wrapper_jp_with_newline(str_input, n_wrap)
        print()
        print(result)
        print("\n> Wrapped\n")
