import sys
import logging
import socket

from checkio_docker.client import DockerClient

from checkio_cli.server.tcpserver import TCPConsoleServer


MEM_LIMIT = '512m'
CPU_SHARES = '512'  # Default 1014
USER_CONNECTION_ID = 1
DOCKER_ID = 2
DOCKER_LINUX_IP = '172.17.42.1'


def is_linux():
    return 'linux' in sys.platform


def get_docker_command():
    if is_linux():
        local_ip = DOCKER_LINUX_IP
    else:
        local_ip = socket.gethostbyname(socket.gethostname())

    command = "{} {} {} {}".format(local_ip, TCPConsoleServer.PORT, USER_CONNECTION_ID, DOCKER_ID)
    logging.debug("Docker args: {}".format(command))
    return command


def start(mission, path=None):
    docker_client = DockerClient()
    if path:
        docker_client.build_mission(mission, path)
        logging.info('Image has build')

    logging.info('Run docker:')
    command = get_docker_command()
    docker_container = docker_client.run(mission, command)

    for line in docker_container.logs(stream=True, logs=True):
        try:
            logging.info(line)
        except Exception as e:
            logging.error(e, exc_info=True)
            pass
