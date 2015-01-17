import operator
from operator import or_, and_, xor, not_

from toolz.curried import curry, first, juxt


eq = curry(operator.eq)
ge = curry(operator.ge)
gt = curry(operator.gt)
le = curry(operator.le)
lt = curry(operator.lt)
ne = curry(operator.ne)


logic_ops = (or_, and_, xor, not_)

@curry
def IN(a, b):
    return operator.contains(b, a)


@curry
def WHERE(conditions, seq, rpn=False):
    if rpn:
        return filter(where_stack(get_conditions(conditions)), seq)
    elif len(conditions) > 1:
        return filter(all_conditions(get_conditions(conditions)), seq)
    return filter(get_condition(*first(conditions)), seq)


@curry
def all_conditions(conditions, d):
    return all(juxt(conditions)(d))


def get_conditions(conditions):
    return [i if i in logic_ops else get_condition(*i) for i in conditions]


@curry
def get_condition(key, operator, value, d):
    return operator(d[key], value)


@curry
def where_stack(conditions, d):
    s = []
    for op in conditions:
        s.append(op(s.pop(), s.pop()) if op in logic_ops else op(d))
    return s.pop()

