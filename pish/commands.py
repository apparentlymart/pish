
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


def reverse(inp):
    return reversed(tuple(inp))


def reduce(inp, f, init=None):
    if init is not None:
        initializer = init()
    else:
        initializer = 0
    def reducewrapper(result, value):
        return f(result=result, value=value)

    return (__builtin__.reduce(reducewrapper, inp, initializer),)


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


def diff(inp, iter1, iter2=None):
    if iter2 is None:
        iter2 = iter1
        iter1 = inp

    t1 = tuple(iter1)
    t2 = tuple(iter2)

    class Hunk(object):
        def __repr__(self):
            return '<Hunk %s %i:%i %i:%i %r to %r>' % (self.action,
                                                       self.oldstart,
                                                       self.oldend,
                                                       self.newstart,
                                                       self.newend,
                                                       self.olditems,
                                                       self.newitems)

    import difflib
    matcher = difflib.SequenceMatcher(None, t1, t2)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        hunk = Hunk()
        hunk.action = tag
        hunk.oldstart = i1
        hunk.oldend = i2
        hunk.newstart = j1
        hunk.newend = j2
        hunk.olditems = t1[i1:i2]
        hunk.newitems = t2[j1:j2]
        yield(hunk)


def cat(inp):
    for it in inp:
        for value in it:
            yield value


def range(inp, start, stop, step=1):
    return xrange(start, stop, step)


def append(inp, other):
    for value in inp:
        yield value
    for value in other:
        yield value


def prepend(inp, other):
    for value in other:
        yield value
    for value in inp:
        yield value


def head(inp, items=10):
    got = 0
    for value in inp:
        yield value
        got = got + 1
        if got == items:
            break


def tail(inp, items=10):
    i1 = iter(inp)
    i2 = iter(inp)

    from collections import deque

    q = deque()

    for value in inp:
        q.append(value)
        if len(q) > items:
            q.popleft()

    return q


def slowdown(inp, delay=1):
    import time
    for value in inp:
        yield value
        time.sleep(delay)


