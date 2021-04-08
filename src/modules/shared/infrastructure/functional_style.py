from functools import reduce


def compose(*fs):
    apply = lambda arg, f: f(arg)
    composition = lambda x: reduce(apply, [x, *fs])
    return composition
