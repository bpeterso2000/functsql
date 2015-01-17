import operator

from toolz.curried import curry, get, keyfilter, pluck

eq = curry(operator.eq)
contains = curry(operator.contains)


@curry
def SELECT(keys, seq):
    return filterkeys(keys, seq)


@curry
def SELECT_VALUE(key, seq):
    return map(get(key), seq)


@curry
def SELECT_VALUES(keys, seq):
    return pluck(keys, seq)


@curry
def AS_LIST(seq):
    return list(seq)


@curry
def filterkey(key, seq):
    return map(keyfilter(eq(key)), seq)


@curry
def filterkeys(keys, seq):
    return map(keyfilter(contains(keys)), seq)
