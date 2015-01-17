from operator import itemgetter

from toolz.curried import curry, pipe


@curry
def ORDER_BY(keys, d):
    keys = [keys] if isinstance(keys, str) else list(keys)
    keys = map(lambda k: (k.lstrip('-+'), k.startswith('-')), reversed(keys))
    funct = curry(lambda k, d: sorted(d, key=itemgetter(k[0]), reverse=k[1]))
    return pipe(d, *map(funct, keys))
