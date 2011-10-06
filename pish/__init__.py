

import pkg_resources


class Pisher(object):
    commands = {}

    def __init__(self):
        group = "pish.commands"
        for entrypoint in pkg_resources.iter_entry_points(group=group):
            name = entrypoint.name
            if name not in self.commands:
                self.commands[name] = entrypoint

    def get_command_impl(self, name):
        return self.commands[name].load()


def main(*argv):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-e", dest="execute",
                      help="a command to execute",
                      metavar="command")

    (options, args) = parser.parse_args()
    return 0


def print_command_results(func, inp=(), kwargs=None):
    if kwargs is None:
        kwargs = {}

    for result in func(inp, **kwargs):
        print repr(result)


