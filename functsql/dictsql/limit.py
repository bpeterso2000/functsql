from pytoolz import curry, drop, take


@curry
def LIMIT(size, seq, offset=0):
    return pipe(seq, drop(offset), take(size))

TOP = LIMIT
