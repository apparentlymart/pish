
import __builtin__


def glob(inp, pattern="*"):
    import glob
    return (x.decode('utf8') for x in glob.iglob(pattern))


def readfile(inp, *fns):
    if len(fns) == 0:
        fns = inp
    files = (file(fn) for fn in fns)
    for f in files:
        for l in f:
            yield l.rstrip("\r\n")


def stat(inp, *fns):
    import os
    if len(fns) == 0:
        fns = inp
    for fn in fns:
        yield os.stat(fn)


def grep(inp, f=lambda x : True):
    return (x for x in inp if f(value=x))


def map(inp, f=lambda x : x):
    return (f(value=x) for x in inp)


def sort(inp, f=None):
    def sortwrapper(x):
        return f(value=x)

    if f is not None:
        f = sortwrapper

    return sorted(inp, key=f)


def getattr(inp, attrname):
    for x in inp:
        yield __builtin__.getattr(x, attrname)


def getkey(inp, key):
    for x in inp:
        yield x[key]


def sum(inp):
    ret = 0
    for x in inp:
        ret = ret + x
    return (ret,)


def regexsearch(inp, regex):
    import re
    for x in inp:
        match = re.search(regex, x)
        if match:
            d = match.groupdict()
            idx = 1
            for s in match.groups():
                d[idx] = s
                idx = idx + 1
            yield d
        else:
            yield {}


def count(inp):
    ret = 0
    for x in inp:
        ret = ret + 1
    return (ret,)


def countuniq(inp):
    ret = {}
    for x in inp:
        if x not in ret:
            ret[x] = 0
        ret[x] = ret[x] + 1
    return (ret,)


def uniq(inp):
    return set(inp)


def zip(inp, iter1, iter2=None):
    if iter2 is None:
        iter2 = iter1
        iter1 = inp

    try:
        while True:
            v1 = iter1.next()
            v2 = iter2.next()
            yield(v1, v2)
    except StopIteration:
        pass

