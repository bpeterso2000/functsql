from pytoolz import curry, drop, pipe, take


@curry
def LIMIT(size, seq, offset=0):
    return pipe(seq, drop(offset), take(size))

TOP = LIMIT
