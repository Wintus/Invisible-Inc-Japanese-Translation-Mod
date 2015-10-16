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


# extract and generalize modification logic as decorator pattern
def str_save(target, holder=str_dummy):
    """Save sub-strings during the process and put them back at the end.

    return Decorator"""

    def decorator(func):
        from functools import wraps
        from collections import Iterable

        @wraps(func)
        def wrapper(*args, **kwargs):
            def replacer_maker(old, new):
                def replacer(x):
                    if isinstance(x, str):
                        return x.replace(old, new)
                    else:
                        return x
                return replacer

            # replace target in string of args
            new_args = map(replacer_maker(target, holder), args)
            result = func(*new_args, **kwargs)
            # recover target in string of output
            if isinstance(result, str):
                return result.replace(holder, target)
            elif isinstance(result, Iterable):
                return map(replacer_maker(holder, target), result)
            else:
                return result
        return wrapper
    return decorator


# and here get the decorated function
# wrapper == str_wrap_save_newline
@str_save('\n')
def wrapper(string, n):
    """Wrap a given string by n-char width keeping CR"""
    return str_wrap(string, n)


def str_wrap_with_newline(string, n, newline='\n'):
    str_list = string.split(newline)
    return newline.join(map(lambda s: str_wrap(s, n), str_list))


def descape(string):
    return string.encode('unicode-escape').decode('utf-8')


def rescape(string):
    return string.encode('utf-8').decode('unicode-escape')


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
