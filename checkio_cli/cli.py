import sys
import argparse
import logging
LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]

parser = argparse.ArgumentParser(description='Command line interface for CheckiO')
parser.add_argument('-v', dest='verbose', default=2, type=int,
                    help='Scripts verbose level')

# there are two kind of command line interfaces.
# the first one is for working with file
# the second one is for working with checking folder and configure

if len(sys.argv) >= 2 and '.' in sys.argv[1]:
    from checkio_cli.interfaces.ifile import use
elif sys.argv[1] == 'git':
    from checkio_cli.interfaces.igit import use
else:
    from checkio_cli.interfaces.ifolder import use


def main():
    if use(parser):
        options = parser.parse_args()
        logging.basicConfig(level=LEVELS[options.verbose])
        options.func(options)
