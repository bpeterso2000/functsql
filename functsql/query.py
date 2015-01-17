from collections import Sequence

from toolz import curry, pipe


SIGNATURE_KEYS = (
    ('s', lambda x: isinstance(x, str)),
    ('S', lambda x: isinstance(x, Sequence)),
    ('w', lambda x: callable(x) and x.__name__ == 'all'),
    ('c', lambda x: callable(x)))


def get_seq_signature(seq):
    for item in seq:
        for key, fn in SIGNATURE_KEYS:
            if fn(item):
                yield key
                break
        else:
            yield '.'


def QUERY(seq, *functs):
    """
    Pipes table through a series of functions
    ---------------------------------------------------------------------------
    return funct1 | funct2 | ...

    :param seq: a sequence of dictionaries (table)
    :type seq: sequence(dict, ...)
    :param *functs: a series of functions to pipe the table through
    :type functs: funct
    :returns: a map of dictionaries
    :rtype: map(dict, ...)
    """
    return pipe(seq, *functs)


@curry
def VIEW(functs, seq):
    return QUERY(seq, *functs)
