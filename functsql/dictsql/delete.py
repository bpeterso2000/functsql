from toolz import curry

from .where import *


@curry
def DELETE_WHERE(conditions, seq, rpn=False):
    if rpn:
        return filter(not_where_stack(get_conditions(conditions)), seq)
    elif len(conditions) > 1:
        return filter(not_all_conditions(get_conditions(conditions)), seq)
    return filter(not_condition(*conditions), seq)


@curry
def not_all_conditions(conditions, d):
    return not all_conditions(conditions, d)


@curry
def not_condition(key, operator, value, d):
    return not get_condition(key, operator, value, d)


@curry
def not_where_stack(conditions, d):
    return not where_stack(conditions, d)
