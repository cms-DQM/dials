import itertools


def list_to_range(i):
    _i = sorted(i)
    for _, b in itertools.groupby(enumerate(_i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]
