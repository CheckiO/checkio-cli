# Console tool for running missions at own computer.
#
# Author: CheckiO <igor@checkio.org>
# Last Change:
# URL: https://github.com/CheckiO/checkio-console

"""
:py:mod:`checkio_console.cli` - Command line interface for CheckiO
==============================================================================
"""

import os
import signal
import argparse
import logging
import coloredlogs

from tornado.ioloop import IOLoop

from checkio_cli.server import tcpserver
from checkio_cli.docker import docker_client
from checkio_cli.native import native_client

logger = logging.getLogger(__name__)


def add_arguments_server(parser_server):
    parser_server.add_argument('-i', '--input-file', help='Input file this data for task')


def add_arguments_docker(parser_docker):
    parser_docker.add_argument('-e', '--environment', help='Mission environment name')
    parser_docker.add_argument('-p', '--path', help='Mission files path for build image',
                               required=False)
    parser_docker.add_argument('-m', '--mission', help='Mission name')


def add_arguments_native(parser_native):
    parser_native.add_argument('-e', '--environment', help='Mission environment name')
    parser_native.add_argument('-p', '--path', help='Mission files path for build image',
                               required=False)
    parser_native.add_argument('-r', '--result', help='Result folder for checkout', default=None)


def parse_args():
    parser = argparse.ArgumentParser(description='Command line interface for CheckiO')
    parser.add_argument('-d', '--debug', help='Debug logging', action='store_true', default=False)

    subparsers = parser.add_subparsers()
    parser_server = subparsers.add_parser('server', help='Run TCPServer')
    add_arguments_server(parser_server)
    parser_server.set_defaults(func=start_server)

    parser_docker = subparsers.add_parser('docker', help='Show information about user')
    add_arguments_docker(parser_docker)
    parser_docker.set_defaults(func=run_docker)

    parser_dserver = subparsers.add_parser('dserver', help='start docker and server')
    add_arguments_docker(parser_dserver)
    add_arguments_server(parser_dserver)
    parser_dserver.set_defaults(func=run_dserver)

    parser_native = subparsers.add_parser('native', help='Run referee without docker')
    add_arguments_native(parser_native)
    parser_native.set_defaults(func=run_native)

    parser_dserver = subparsers.add_parser('nserver', help='start both processes')
    add_arguments_native(parser_dserver)
    add_arguments_server(parser_dserver)
    parser_dserver.set_defaults(func=run_dserver)

    return parser.parse_args()


def start_server(options):
    def exit_signal(sig, frame):
        logging.info("Trying exit")
        if docker_client.docker_container is not None:
            docker_client.docker_container.stop()
            docker_client.docker_container.remove_container()
        io_loop.add_callback(IOLoop.instance().stop)

    signal.signal(signal.SIGINT, exit_signal)
    signal.signal(signal.SIGTERM, exit_signal)

    io_loop = IOLoop.instance()
    tcpserver.start(options.input_file, io_loop)
    io_loop.start()


def run_dserver(options):
    if os.fork():
        run_docker(options)
    else:
        start_server(options)


def run_docker(options):
    docker_client.start(options.mission, options.environment, options.path)


def run_native(options):
    native_client.start(options.result, options.environment, options.path)


def config_logging(options):
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    coloredlogs.install()


def main():
    options = parse_args()

    config_logging(options)
    logging.info('Run...')
    try:
        options.func(options)
    except Exception as e:
        logging.error(e, exc_info=True)


if __name__ == '__main__':
    main()
