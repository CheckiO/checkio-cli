import sys
import os
import logging
import socket
from distutils.dir_util import copy_tree

from checkio_docker.client import DockerClient
from checkio_cli import config
from checkio_cli.folder import Folder


def is_linux():
    return 'linux' in sys.platform


def start_native(path, python3):
    try:
        os.chdir(path)
        os.system(python3 + ' main.py 127.0.0.1 ' +
                  str(config.CONSOLE_SERVER_PORT) + ' 1 2 ' + str(logging.root.level))
    finally:
        os.chdir('.')


def start_docker(slug):
    if is_linux():
        local_ip = config.DOCKER_LINUX_IP
    else:
        local_ip = socket.gethostbyname(socket.gethostname())

    command = "{} {} 1 2 {}".format(local_ip, config.CONSOLE_SERVER_PORT, str(logging.root.level))
    docker_client = DockerClient()
    folder = Folder(slug)
    copy_tree(folder.verification_folder_path(), folder.container_verification_folder_path())
    docker_container = docker_client.run(slug, command, volumes={
        '/opt/mission/src': folder.compiled_referee_folder_path(),
        '/opt/mission/envs': folder.compiled_envs_folder_path()
    })
    for line in docker_container.logs(stream=True, logs=True):
        try:
            logging.info(line)
        except Exception as e:
            logging.error(e, exc_info=True)
            pass


def start_server(slug, server_script, action, path_to_code, python3, env_name=None):
    os.system(' '.join((python3, server_script, slug, action, env_name, path_to_code,
              str(config.CONSOLE_SERVER_PORT), str(logging.root.level))))


def execute_referee(command, slug, interpreter, without_container=False, interface_child=False,
                    referee_only=False, interface_only=False):
    # TODO: killing server after words
    def start_interface():
        return start_server(slug, folder.interface_cli_main(), command, folder.solution_path(),
                            folder.native_env_bin('python3'), interpreter)

    def start_container():
        return start_docker(slug)

    def start_local():
        return start_native(folder.referee_folder_path(), folder.native_env_bin('python3'))

    folder = Folder(slug)
    if interface_only:
        return start_interface()

    if referee_only:
        if without_container:
            return start_local()
        else:
            return start_container

    pid_child = os.fork()
    start_interface_first = bool(pid_child)
    if interface_child:
        start_interface_first = not start_interface_first

    if start_interface_first:
        return start_interface()
    else:
        if without_container:
            return start_local()
        else:
            return start_container()


def run_home(mission, interpreter, without_container):
    raise NotImplementedError("Running for {} {} is not implemented yer".
                              format(mission, interpreter))


def console_home(mission, interpreter, without_container):
    raise NotImplementedError("Running in console for {} {} is not implemented yer".
                              format(mission, interpreter))


def sandbox_home(mission, interpreter, without_container):
    raise NotImplementedError("Running in sandbox for {} {} is not implemented yer".
                              format(mission, interpreter))
