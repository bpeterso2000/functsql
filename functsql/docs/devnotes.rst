The following is a loose description of the functions
(not all are fully implmented yet) ...

INSERT([key|(keys)], value|(values)|items)
SELECT(([reduce-fn], [*|key-in|(keys)], [fn|(functs)], [key-out], [default]), ...)
UPDATE((*|key-in|(keys), fn|(functs), key-out)
UPDATE_WHERE((*|key-in|(keys), fn|(functs), key-out, condition|(conditions)), ...)
WHERE((condition|(conditions)), ...)
[LEFT|RIGHT|CROSS] [INNER|OUTER] JOIN((table, left-key, [right-key]), ...)
GROUP_BY(key|(keys), [(*|key-in|(keys), reduce-fn, [key-out])])
ORDER_BY(key|(keys))
LIMIT(size, offset)
DELETE_WHERE((condition|(conditions)), ...)
DROP key|(keys)


keymap_
keymap_as
keyfilter_
keyreduce_
keyreduce_as
itemmap
itemmap_as
itemfilter
itemreduce
itemreduce_as
renamekey
delkey
getkey
getkey_as
updatekey
updatekey_as

condition



Functionality
-------------
keymap_ --> pipe(seq, getkeys(keys), valmap(fn))
keymap_as --> pipe(seq, keymap(keyin), rename(keyin, keyout))
keyfilter_ --> (d for d in seq if fn(d[key]))
keyreduce_--> ({key: fn(keyfilter(key, d))},)
keyreduce_as --> ({keyout: fn(keyfilter_(keyin, d))},)
itemmap --> map
itemmap_as --> ({keyout: fn(d)} for d in seq)
itemfilter --> filter(fn, seq)
itemreduce --> fn(seq)
itemreduce_as --> ({keyout: itemreduce(d)},)
renamekey --> keymap(lambda k: newkey if k == oldkey else k, seq)
delkey --> (toolz.dissoc(d, key) for d in seq)
getkeys --> toolz.pluck(keys, seq)
getkey_as --> pipe(seq, getkeys(keyin), rename(keyin, keyout))
updatekey --> (toolz.update_in(d, keys, value) for d in seq)
as_values --> map(toolz.get(keys), seq)
as_list --> list(seq)
as_tuple --> tuple(seq)
as_dict --> (dict(zip(keys, v)) for v in seq)


Signatures
----------
keymap(keys, fn, seq)
keymap_as(keyin, fn, keyout, seq)
keyfilter_(key, fn, seq)
keyreduce_(key, fn, seq)
keyreduce_as(keyin, fn, keyout, seq)
itemmap(fn, seq)
itemmap_as(fn, keyout, seq)
itemfilter(fn, seq)
itemreduce(fn, seq)
itemreduce_as(fn, keyout, seq)
renamekey(oldkey, newkey, seq)
delkey(key, seq)
getkey(key, seq)
getkey_as(keyin, keyout, seq)
updatekey(key, value, seq)
as_values(seq)
as_list(seq)
as_tuple(seq)
as_dict(keys, seq)

INSERT
------
S        toolz.concat(items, seq)
d        toolz.cons(d, seq)
s[^Scw]  toolz.cons(dict(d), seq)
SS       toolz.concat(as_dict(keys, items), seq)

FROM_CSV
--------
open CSV dict reader yield results
filename, sep

FROM_JSON
---------
filename, root_node


SELECT
------
SELECT(([reduce-fn], [*|key-in|(keys)], [fn|(functs)], [key-out], [default]), ...)


