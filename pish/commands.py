

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


def grep(inp, f=lambda x : True):
    return (x for x in inp if f(x))


def map(inp, f=lambda x : x):
    return (f(x) for x in inp)


def sort(inp, f=None):
    return sorted(inp, key=f)
