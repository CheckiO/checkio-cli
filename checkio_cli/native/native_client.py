import os

from checkio_docker.parser import MissionFilesHandler
from checkio_cli.server.tcpserver import TCPConsoleServer


def start(result, environment, path):
    mission_source = MissionFilesHandler(environment, result)
    try:
        mission_source.compile_from_files(path)
    except:
        pass
    folder = mission_source.path_verification
    try:
        os.chdir(os.path.join(folder, 'src'))
        os.system('python3 main.py 127.0.0.1 ' + str(TCPConsoleServer.PORT) + ' 1 2')
    finally:
        os.chdir('.')
