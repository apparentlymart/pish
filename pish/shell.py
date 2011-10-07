
import os
import os.path
import pish
from pish.parser import parse_command_line


def main(*argv):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-e", dest="execute",
                      help="a command to execute",
                      metavar="command")

    (options, args) = parser.parse_args()

    return repl()
    return 0


def repl():
    import readline
    import atexit
    import traceback
    histfile = os.path.expanduser("~/.pish_history")
    try:
        readline.read_history_file(histfile)
    except IOError:
        # Don't care. We'll make a file on exit, hopefully.
        pass
    atexit.register(readline.write_history_file, histfile)

    pisher = pish.Pisher()

    while True:
        try:
            cmd_str = raw_input("> ")
            cmd_line = parse_command_line(cmd_str)
            print repr(cmd_line)
        except EOFError:
            print ""
            return 0
        except KeyboardInterrupt:
            pass
        except:
            traceback.print_exc()





