
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


def sum(inp):
    ret = 0
    for x in inp:
        ret = ret + x
    return (ret,)

