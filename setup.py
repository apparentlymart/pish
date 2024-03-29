
from setuptools import setup
from os.path import join, dirname

try:
    long_description = open(join(dirname(__file__), 'README.rst')).read()
except Exception:
    long_description = None

setup(
    name='pish',
    version='0.1',
    description='Python-powered Shell',
    author='Martin Atkins',
    author_email='mart@degeneration.co.uk',

    long_description=long_description,

    packages=['pish'],
    provides=['pish'],
    requires=['setuptools'],

    entry_points={
        "pish.commands": [
            "glob = pish.commands:glob",
            "readfile = pish.commands:readfile",
            "exec = pish.commands:exec_",
            "stat = pish.commands:stat",
            "grep = pish.commands:grep",
            "map = pish.commands:map",
            "sort = pish.commands:sort",
            "uniq = pish.commands:uniq",
            "getattr = pish.commands:getattr",
            "getkey = pish.commands:getkey",
            "sum = pish.commands:sum",
            "regexsearch = pish.commands:regexsearch",
            "regexsplit = pish.commands:regexsplit",
            "count = pish.commands:count",
            "countuniq = pish.commands:countuniq",
            "zip = pish.commands:zip",
            "diff = pish.commands:diff",
            "cat = pish.commands:cat",
            "reverse = pish.commands:reverse",
            "reduce = pish.commands:reduce",
            "range = pish.commands:range",
            "append = pish.commands:append",
            "prepend = pish.commands:prepend",
            "head = pish.commands:head",
            "tail = pish.commands:tail",
            "skip = pish.commands:skip",
            "slowdown = pish.commands:slowdown",
        ],
    },
)

