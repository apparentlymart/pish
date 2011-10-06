

def ls(inp, pattern="*"):
    import glob
    return glob.iglob(pattern)


def cat(inp, *fns):
    files = (file(fn) for fn in fns)
    for f in files:
        for l in f:
            yield l.rstrip("\r\n")


def grep(inp, f):
    return (x for x in inp if f(x))


def map(inp, f):
    return (f(x) for x in inp)
