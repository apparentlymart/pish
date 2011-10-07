
from pyparsing import *
import re


class Command(object):
    def __init__(self, match, location, tokens):
        self.cmd_name = tokens[0]
        self.params = tokens[1]

    def __repr__(self):
        return "<Command %r %r>" % (self.cmd_name, self.params.exprs)


class PythonLambda(object):
    def __init__(self, match, location=None, tokens=()):
        self.expr = match[1:-1].strip()
        self.code = compile(self.expr, '<expr>', 'eval', dont_inherit=True)

    def __repr__(self):
        return "<PythonLambda {%s}>" % self.expr


class Literal(object):
    def __init__(self, match, location, tokens):
        self.value = tokens

    def __repr__(self):
        return "<Literal %s>" % self.value


class Option(object):
    def __init__(self, match, location, tokens):
        self.name = tokens[1]
        self.expr = tokens[3]

    def __repr__(self):
        return "<Option %r: %r>" % (self.name, self.expr)

class CmdLine(object):

    def __init__(self, match, location, tokens):
        self.parts = [ x for x in tokens if x != "|" ]

    def __repr__(self):
        return "<CmdLine %r>" % self.parts


class Params(object):
    def __init__(self, match, location, tokens):
        self.exprs = tokens[:]

    def __repr__(self):
        return "<Params %r>" % self.exprs


def transform_unquoted_literal(match, location, tokens):
    value = tokens[0]
    if value.isdigit():
        return int(value)
    elif value == "True":
        return True
    elif value == "False":
        return False
    elif re.match('\d+\.\d+$', value):
        return float(value)
    else:
        return value.decode('utf8')


cmd_name = Word(alphas)
unquoted_literal = Word(alphanums + '.').setParseAction(transform_unquoted_literal)
literal = (QuotedString(quoteChar='"', escChar='\\') | unquoted_literal).setParseAction(Literal)
python_lambda = nestedExpr("{", "}", ignoreExpr=dblQuotedString | sglQuotedString).setParseAction(PythonLambda)

expr = python_lambda | literal

option = ("--" + Word(alphanums) + Optional("=" + expr)).setParseAction(Option)
params = ZeroOrMore(expr | option).setParseAction(Params)
command = (cmd_name + params).setParseAction(Command)

cmd_line_part = (command | python_lambda)

cmd_line = (cmd_line_part + ZeroOrMore("|" + cmd_line_part)).setParseAction(CmdLine)


def parse_command_line(line):
    return cmd_line.parseString(line, parseAll=True)[0]