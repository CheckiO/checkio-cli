import os
import shutil

from checkio_cli.server.tcpserver import TCPConsoleServer

from checkio_docker.parser import MissionFilesCompiler

DEFAULT_DIST = 'dist'
DIST_SUB_FOLDER = 'checkio-mission'


def start(path, compiled_path):
    if not compiled_path:
        compiled_path = os.path.join(path, DEFAULT_DIST)

    compiled_path = os.path.join(compiled_path, DIST_SUB_FOLDER)
    if os.path.exists(compiled_path):
        shutil.rmtree(compiled_path)

    mission_source = MissionFilesCompiler(compiled_path)
    mission_source.compile(source_path=path)
    _run_script(mission_source.path_verification)


def _run_script(path):
    try:
        os.chdir(os.path.join(path, 'src'))
        os.system('python3 main.py 127.0.0.1 ' + str(TCPConsoleServer.PORT) + ' 1 2')
    finally:
        os.chdir('.')
