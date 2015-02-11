# Console tool for running missions at own computer.
#
# Author: CheckiO <igor@checkio.org>
# Last Change:
# URL: https://github.com/CheckiO/checkio-console

"""
:py:mod:`checkio_console.cli` - Command line interface for CheckiO
==============================================================================
"""

import signal
import argparse
import logging
import sys
import textwrap
import coloredlogs
from threading import Thread

from tornado.ioloop import IOLoop

from checkio_cli import tcpserver, docker_client

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Command line interface for CheckiO')
parser.add_argument('-e', '--environment', help='Mission environment name', required=False)
parser.add_argument('-p', '--path', help='Mission files path for build image')
parser.add_argument('-m', '--mission', help='Mission name', required=False)
parser.add_argument('-i', '--input-file', help='Input file this data for task', required=False)
options = parser.parse_args()


def main():
    """The command line interface for the ``checkio`` program."""
    def exit_signal(sig, frame):
        logging.info("Trying exit")
        if docker_client.docker_instance is not None:
            docker_client.docker_instance.stop()
            docker_client.docker_instance.remove_container()
        io_loop.add_callback(IOLoop.instance().stop)

    signal.signal(signal.SIGINT, exit_signal)
    signal.signal(signal.SIGTERM, exit_signal)

    if not options:
        usage()
        sys.exit(0)

    coloredlogs.install()
    logging.info('Run...')

    io_loop = IOLoop.instance()
    if options.input_file:
        thread_tcpserver = Thread(target=tcpserver.thread_start, args=(options.input_file, io_loop))
        thread_tcpserver.start()
    else:
        if not options.mission or not options.environment:
            print('path, mission, and environment is required args')
            sys.exit()
        docker_client.start(options.mission, options.environment, options.path)

    io_loop.start()


def usage():
    """Print a usage message to the terminal."""
    print(textwrap.dedent("""
        Usage: checkio-cli [ARGS]
        The checkio-cli ....
        For more information please refer to the GitHub project page
        at https://github.com/CheckiO/checkio-cli
    """).strip())


if __name__ == '__main__':
    main()
