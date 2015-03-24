import os
import shutil
import tempfile
from distutils.dir_util import copy_tree

from checkio_cli.server.tcpserver import TCPConsoleServer
from checkio_docker.parser import MissionFilesCompiler

DEFAULT_DIST = 'dist'
DIST_SUB_FOLDER = 'checkio-mission'


def start(path, destination_path):
    if not destination_path:
        destination_path = os.path.join(path, DEFAULT_DIST)

    destination_path = os.path.join(destination_path, DIST_SUB_FOLDER)
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

    work_path = tempfile.mkdtemp()
    try:
        mission_source = MissionFilesCompiler(work_path)
        mission_source.compile_from_files(path)
        copy_tree(work_path, destination_path)
    finally:
        if os.path.exists(work_path):
            shutil.rmtree(work_path)
    _run_script(destination_path)


def _run_script(path):
    try:
        os.chdir(os.path.join(path, 'verification', 'src'))
        os.system('python3 main.py 127.0.0.1 ' + str(TCPConsoleServer.PORT) + ' 1 2')
    finally:
        os.chdir('.')
