import sys
import os
import signal
import logging
import socket

from tornado.ioloop import IOLoop

from checkio_docker.client import DockerClient
from checkio_cli import config
from checkio_cli.server import tcpserver
from checkio_cli.folder import Folder


def is_linux():
    return 'linux' in sys.platform


def start_native(path, python3):
    try:
        os.chdir(path)
        os.system(python3 + ' main.py 127.0.0.1 ' +
                  str(config.CONSOLE_SERVER_PORT) + ' 1 2')
    finally:
        os.chdir('.')


def start_docker(slug):
    if is_linux():
        local_ip = config.DOCKER_LINUX_IP
    else:
        local_ip = socket.gethostbyname(socket.gethostname())

    command = "{} {} 1 2".format(local_ip, config.CONSOLE_SERVER_PORT)
    docker_client = DockerClient()
    docker_container = docker_client.run(slug, command)
    for line in docker_container.logs(stream=True, logs=True):
        try:
            logging.info(line)
        except Exception as e:
            logging.error(e, exc_info=True)
            pass


def start_server(user_data):
    def exit_signal(sig, frame):
        logging.info("Trying exit")
        io_loop.add_callback(IOLoop.instance().stop)

    signal.signal(signal.SIGINT, exit_signal)
    signal.signal(signal.SIGTERM, exit_signal)

    io_loop = IOLoop.instance()
    tcpserver.start(user_data, io_loop)
    io_loop.start()


def check_home(slug, interpreter, without_container):
    # TODO: killing server after words
    folder = Folder(slug)
    pid_child = os.fork()
    if pid_child:
        if without_container:
            start_native(folder.referee_folder_path(), folder.native_env_bin('python3'))
        else:
            start_docker(slug)
    else:
        start_server({
            'action': 'check',
            'code': folder.solution_code(),
            'env_name': interpreter or config.ACTIVE_INTERPRETER
        })


def run_home(mission, interpreter, without_container):
    raise NotImplementedError("Running for {} {} is not implemented yer".
                              format(mission, interpreter))


def console_home(mission, interpreter, without_container):
    raise NotImplementedError("Running in console for {} {} is not implemented yer".
                              format(mission, interpreter))


def sandbox_home(mission, interpreter, without_container):
    raise NotImplementedError("Running in sandbox for {} {} is not implemented yer".
                              format(mission, interpreter))
