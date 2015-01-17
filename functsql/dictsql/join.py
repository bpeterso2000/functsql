from toolz.curried import curry, join, merge


@curry
def JOIN(item, leftseq):
    """
    --- future ---
    elif len(item) == 3:
        # used to add prefix to keys to avoid conflicting name space
        rightseq, leftkey, rightkey, key_prefix = item
    """
    if len(item) == 2:
        rightseq, leftkey = item
        rightkey = leftkey
    elif len(item) == 3:
        rightseq, leftkey, rightkey = item
    return map(merge, join(leftkey, leftseq, rightkey, rightseq))
