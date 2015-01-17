import sys

from toolz.curried import cons, curry, groupby, pipe, pluck


GROUP_BY = groupby


@curry
def REDUCE_BY(key, reducers, seq):
    return pipe(seq, groupby(key), reducegroups(key, reducers))


@curry
def reducegroups(key, reducers, seq, keyfmt='{fname}:{key}'):
    keys = [keyfmt.format(fname=fn.__name__, key=key)
            for fn, key in tuple(reducers)]
    for group, values in seq.items():
        reduced_vals = (pluckreduce(f, k, values) for f, k in reducers)
        yield dict(cons((key, group), zip(keys, reduced_vals)))


@curry
def pluckreduce(fn, key, seq):
    return pipe(seq, pluck(key), fn)
