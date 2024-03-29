========================================
pish -- shell-like Python data wrangling
========================================

``pish`` allows you to wrangle Python data using a shell-like
language.

In UNIX, a command reads input from stdin and produces
results on stdout. ``pish`` takes this interface and
applies it instead to Python iterables.

``pish`` is really just a toy I threw together in a few hours
during PyCodeConf 2011 in Miami, FL as an application of various
cool things I learned or was inspired by:

* Python allows functions that deal in iterables to be chained together like UNIX pipes, as pointed out by Raymond Hettinger in his "Python is Awesome" talk.

* PyParsing makes it easy to put together a parser for an arbitrary machine language very quickly.

* Entry Points are an interesting mechanism for decentralized extensibility of Python apps.

* Code really is a first-class object in Python: raw code objects, the `compile` function and AST wrangling are really powerful and supplied as standard.

Examples
--------

A pish statement is a list of commands separated by the pipe (`|`)
character. Just as with shell pipes, the output from one command
is the input to the next.

The first command in a statement must be one that can generate output
given empty input, because the input to the first command is always
empty. `glob` is an example of such a command::

    > glob "example/*"
    u'example/example1.pl'
    u'example/example6.py'
    u'example/example3.java'
    u'example/example1.py'
    u'example/example1.java'
    u'example/example2.py'
    u'example/example2.java'
    u'example/example3.py'
    u'example/example2.pl'
    u'example/example5.py'
    u'example/example4.py'

As you can see, the shell just prints out whatever Python values are
yielded from the command. In this case, the results are all strings.

A second command in the statement consumes and transforms the output
from the first::

    > glob "example/*" | regexsearch "(\w+)$"
    {1: u'pl'}
    {1: u'py'}
    {1: u'java'}
    {1: u'py'}
    {1: u'java'}
    {1: u'py'}
    {1: u'java'}
    {1: u'py'}
    {1: u'pl'}
    {1: u'py'}
    {1: u'py'}

The above shows that while UNIX streams are bytestreams often
interpreted as strings separated by newlines, pish streams can
be any Python value.

Different commands expect different types of value as input,
but most of the time we ultimately want to get strings for
human consumption, so there are commands provided to pull
certain keys or attributes from objects::

    > glob "example/*" | regexsearch "(\w+)$" | getkey 1
    u'pl'
    u'py'
    u'java'
    u'py'
    u'java'
    u'py'
    u'java'
    u'py'
    u'pl'
    u'py'
    u'py'

And now we're back to strings, which allows us to do this::

    > glob "example/*" | regexsearch "(\w+)$" | getkey 1 | uniq | sort
    u'java'
    u'pl'
    u'py'

Some commands only produce a single result no matter how much input they get::

    > glob "example/*" | regexsearch "(\w+)$" | getkey 1 | uniq | count
    3
    > glob "example/*" | regexsearch "(\w+)$" | getkey 1 | countuniq
    {u'java': 3, u'pl': 2, u'py': 6}

Some commands except lambda functions that use Python expression syntax
for dynamic behavior::

    > glob "example/*" | regexsearch "(\w+)$" | getkey 1 | uniq | grep { value[0] == "p" }
    u'py'
    u'pl'

This lambda syntax can also be used as a command in its own right, allowing
arbitrary python expressions to generate data::

    > { (6,1,2,2,3,3,3,4,5,6) } | uniq
    1
    2
    3
    4
    5
    6

The input to a command-level lambda is available in the scope of the lambda
as `inp`::

    > glob "example/*" | { (x.upper() for x in inp) }
    u'EXAMPLE/EXAMPLE1.PL'
    u'EXAMPLE/EXAMPLE6.PY'
    u'EXAMPLE/EXAMPLE3.JAVA'
    u'EXAMPLE/EXAMPLE1.PY'
    u'EXAMPLE/EXAMPLE1.JAVA'
    u'EXAMPLE/EXAMPLE2.PY'
    u'EXAMPLE/EXAMPLE2.JAVA'
    u'EXAMPLE/EXAMPLE3.PY'
    u'EXAMPLE/EXAMPLE2.PL'
    u'EXAMPLE/EXAMPLE5.PY'
    u'EXAMPLE/EXAMPLE4.PY'

Some commands take whole statements as parameters. An example of
this is `append`, which allows new items to be added onto the end of a stream:

    > range 1 5 | append <range 10 14>
    1
    2
    3
    4
    10
    11
    12
    13

Command Interface
-----------------

New commands can be added using the entrypoint mechanism.

Just declare an entrypoint in the `pish.commands` group named
after the command you want to add.

The function you refer to must support the following interface:

* the first positional argument is an interable representing the
  input stream. Conventionally this is called `inp`.

* any positional arguments passed after the command name in a statement
  become further positional arguments to this function.

* any arguments of the form `--key=value` will be passed in as keyword
  arguments to the function.

* the function must return something iterable which is the output stream.
  (If the function only returns one value, just return a one-element tuple
  containing the value.)

The parameters to the command are marshalled from the provided parameter
list as follows:

* an unquoted literal that consists only of digits will be passed as an `int`.

* an unquoted literal with two sets of digits separated by a period will be passed
  as a `float`.

* an unquoted literal that is exactly `True` or `False` will be passed as a `bool`.

* a quoted literal will always be passed as a string.

* a lambda function will be passed as a callable whose kwargs become the global
  scope in which the provided expression is evaluated.

* an inline statement will be passed as an iterable that returns the results of
  the statement.

