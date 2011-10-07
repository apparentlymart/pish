

import pkg_resources


class CommandWrapper(object):
    def __init__(self, pisher):
        self.pisher = pisher

    def __getattr__(self, name):
        impl = self.pisher.get_command_impl(name)
        def ret(inp=(), *args, **kwargs):
            return impl(inp, *args, **kwargs)
        ret.__name__ = name
        return ret


class Pisher(object):
    _commands = {}

    def __init__(self):
        group = "pish.commands"
        self.commands = CommandWrapper(self)
        for entrypoint in pkg_resources.iter_entry_points(group=group):
            name = entrypoint.name
            if name not in self._commands:
                self._commands[name] = entrypoint

    def get_command_impl(self, name):
        return self._commands[name].load()


def print_command_results(func, inp=(), kwargs=None):
    if kwargs is None:
        kwargs = {}

    for result in func(inp, **kwargs):
        print repr(result)


