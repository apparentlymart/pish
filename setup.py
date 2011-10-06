
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
            "ls = pish.commands:ls",
            "cat = pish.commands:cat",
            "grep = pish.commands:grep",
            "map = pish.commands:map",
        ],
    },
)

