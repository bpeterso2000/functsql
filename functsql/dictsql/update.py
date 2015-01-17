from toolz import curry, juxt

from .where import *


@curry
def UPDATE(setting, seq):
    into_key = setting[2] if len(setting) == 3 else setting[0]
    return map(valmapkey(*setting[:2], into_key=into_key), seq)


@curry
def UPDATE_WHERE(setting, conditions, seq):
    into_key = setting[3] if len(setting) == 3 else setting[0]
    funct = valmapkey(*setting[:2], into_key=into_key)
    return map(valmap_conditions(funct, get_conditions(conditions)), seq)


@curry
def conditional_valmap(funct, condition, d):
    return funct(d) if condition(d) else d


@curry
def valmap_conditions(funct, conditions, d):
    return funct(d) if all(juxt(conditions)(d)) else d


@curry
def valmapkey(from_key, funct, d, into_key=None):
    d[into_key] = funct(d[from_key])
    return d
