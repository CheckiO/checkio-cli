import sys
import argparse
import logging
LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]

parser = argparse.ArgumentParser(description='Command line interface for CheckiO')
parser.add_argument('-v', dest='verbose', default=2, type=int,
                    help='Scripts verbose level')

# start configuration process at the first start
from checkio_cli.config import settings
if not settings.IS_CONFIGURED:
    from checkio_cli.config.initial_config import console_interactive
    console_interactive()

# there are three kinds of command line interfaces.

if len(sys.argv) >= 2 and '.' in sys.argv[1]:
    # the first one is for working with solution file
    # through the direct call like ./solutin.py
    from checkio_cli.interfaces.ifile import use
elif len(sys.argv) >= 2 and sys.argv[1] == 'mgit':
    # the second one is for mission authors
    # so they can get access to missions git repository from any place
    # checkio-cli git crystal-row status
    from checkio_cli.interfaces.igit import use
else:
    # the third one is for more general using
    # checkio-cli get-git https://github.com/Checkio-Game-Missions/checkio-empire-roman-numerals roman-numbers
    # checkio-cli check roman-numbers
    from checkio_cli.interfaces.ifolder import use


def main():
    if use(parser):
        options = parser.parse_args()
        logging.basicConfig(level=LEVELS[options.verbose])
        options.func(options)
