import os
import git
import shutil

from checkio_cli import config
from checkio_docker.parser import MissionFilesCompiler
from checkio_cli.folder import Folder
from checkio_docker.client import DockerClient


def mission_git_getter(url, slug):
    # TODO: checkout into mission solder
    # compile it
    # build docker
    # prepare cli interface
    folder = Folder(slug)
    destination_path = folder.mission_folder()

    if os.path.exists(destination_path):
        answer = raw_input('Folder {} exists already.'
                           ' Do you want to overwite it? [y]/n :'.format(destination_path))
        if answer is '' or answer.lower().startswith('y'):
            shutil.rmtree(destination_path)
        else:
            return
    try:
        repo = git.Repo.clone_from(url, destination_path)
    except git.GitCommandError as e:
        raise Exception(u"{}, {}".format(e or '', e.stderr))
    folder.mission_config_write({
        'type': 'git',
        'url': url
    })
    print('Prepare mission {} from {}'.format(slug, url))


MISSION_GETTERS = {
    'git': mission_git_getter
}

def rebuild_native(slug):
    folder = Folder(slug)
    if os.path.exists(folder.native_env_folder_path()):
        shutil.rmtree(folder.native_env_folder_path())

    os.system("virtualenv --system-site-packages -p python3 " + folder.native_env_folder_path())
    os.system("{pip3} install -r {requirements}".format(
        pip3=folder.native_env_bin('pip3'),
        requirements=folder.referee_requirements()
    ))
    os.system("{pip3} install -r {requirements}".format(
        pip3=folder.native_env_bin('pip3'),
        requirements=folder.interface_cli_requirements()
    ))


def rebuild_mission(slug):
    folder = Folder(slug)
    docker = DockerClient()
    docker.build(name_image=folder.image_name(), path=folder.verification_folder_path())


def recompile_mission(slug):
    folder = Folder(slug)
    compiled_path = folder.compiled_folder_path()
    if os.path.exists(compiled_path):
        shutil.rmtree(compiled_path)

    mission_source = MissionFilesCompiler(compiled_path)
    mission_source.compile(source_path=folder.mission_folder())
