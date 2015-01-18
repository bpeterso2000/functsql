import collections
import operator

from toolz.curried import complement, curry, keyfilter, pipe, pluck, keymap

eq = curry(operator.eq)
ne = curry(operator.ne)
in_ = curry(operator.contains)
not_in = curry(complement(operator.contains))

string = lambda x: isinstance(x, str)
sequence = lambda x: not string(x) and isinstance(x, collections.Sequence)


@curry
def AS(type_, seq):
    return type_(seq)


@curry
def DROP(keys, seq):
    return dropkeys(keys, seq)


@curry
def RENAME(keys, seq):
    _, aliases = _keynames_n_aliases(keys)
    return renamekeys(aliases, seq)


@curry
def SELECT(keys, seq):
    """
    usage: SELECT([key|(key, alias), ...], seq)

    examples:
    SELECT(('key1',))
    SELECT(('key1', 'key2', ('key3', 'newkey3'), 'key4'))
    """
    keys, aliases = _keynames_n_aliases(keys)
    functs = [getkeys(keys) if len(keys) > 1 else getkey(keys[0])]
    if aliases:
        functs.append(renamekeys(aliases))
    return pipe(seq, *functs)


@curry
def SELECT_VALUES(keys, seq):
    return pluck(keys, seq)


def _keynames_n_aliases(keys):
    aliases = {k[0]: k[1] for k in keys if not string(k)}
    keys = tuple(k if string(k) else k[0] for k in keys)
    return keys, aliases


@curry
def dropkey(key, seq):
    return map(keyfilter(ne(key)), seq)


@curry
def dropkeys(key, seq):
    return map(keyfilter(not_in(key)), seq)


@curry
def getkey(key, seq):
    return map(keyfilter(eq(key)), seq)


@curry
def getkeys(keys, seq):
    return map(keyfilter(in_(keys)), seq)


@curry
def renamekeys(aliases, seq):
    "aliases is a dict with oldnames as keys and new names as values"
    return keymap(lambda k: aliases.get(k, k), seq)
