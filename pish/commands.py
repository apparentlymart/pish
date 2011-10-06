

def ls(inp, pattern="*"):
    import glob
    return glob.iglob(pattern)


def cat(inp, fn):
    return (x.rstrip("\r\n") for x in file(fn))


def grep(inp, f):
    return (x for x in inp if f(x))


def map(inp, f):
    return (f(x) for x in inp)
