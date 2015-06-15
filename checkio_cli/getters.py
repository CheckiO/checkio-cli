import os
import git
import re
import shutil
from distutils.dir_util import copy_tree
import logging

from checkio_docker.parser import MissionFilesCompiler
from checkio_cli.folder import Folder
from checkio_docker.client import DockerClient
from checkio_cli.config import settings


RE_REPO_BRANCH = re.compile('(.+?)\@([\w\-\_]+)$')


class GetterExeption(Exception):
    pass


class TemplateWasntFound(GetterExeption):
    def __init__(self, template, folders):
        self.template = template
        self.folders = folders

    def __str__(self):
        return 'Template "{}"" wasn\'t found in folder(s) "{}"'.format(
            self.template, '","'.join(self.folders)
        )


class MissionFolderExistsAlready(GetterExeption):
    def __init__(self, folder):
        self.folder = folder

    def __str__(self):
        return 'Mission folder "{}" exists already'.format(self.folder)


def make_mission_from_template(mission, template, force_remove=False):
    template_full_path = None
    for template_folder in settings.TEMPLATES_FOLDERS:
        template_full_path = os.path.join(template_folder, template)
        if os.path.exists(template_full_path):
            break
        else:
            template_full_path = None

    if template_full_path is None:
        raise TemplateWasntFound(template, settings.TEMPLATES_FOLDERS)

    folder = Folder(mission)
    mission_folder = folder.mission_folder()
    if os.path.exists(mission_folder):
        if force_remove:
            shutil.rmtree(mission_folder)
        else:
            raise MissionFolderExistsAlready(mission_folder)

    os.mkdir(mission_folder)

    from distutils.dir_util import copy_tree
    copy_tree(os.path.join(template_full_path, 'source'), mission_folder)

    GG = {}
    exec(open(os.path.join(template_full_path, 'run.py')).read()) in GG
    GG['run'](mission)

    folder.mission_config_write({
        'type': 'local',
        'url': mission_folder
    })


def mission_git_init(mission, original_url):
    folder = Folder(mission)
    mission_folder = folder.mission_folder()
    logging.info('Init git repository for folder %s', mission_folder)
    repo = git.Repo.init(mission_folder)
    for root, dirs, files in os.walk(mission_folder):
        if root.endswith('.git') or '/.git/' in root:
            continue

        for file_name in files:
            abs_file_name = os.path.join(root, file_name)
            logging.debug('add file to local git repository %s', abs_file_name)
            repo.index.add([abs_file_name])

    repo.index.commit("initial commit")
    origin = repo.create_remote('origin', original_url)
    origin.push(repo.refs)
    origin.fetch()
    repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
    folder.mission_config_write({
        'type': 'git',
        'url': original_url
    })


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

    re_ret = re.search(RE_REPO_BRANCH, url)
    if re_ret:
        checkout_url, branch = re_ret.groups()
    else:
        checkout_url = url
        branch = 'master'

    try:
        git.Repo.clone_from(checkout_url, destination_path, branch=branch)
    except git.GitCommandError as e:
        raise Exception(u"{}, {}".format(e or '', e.stderr))
    folder.mission_config_write({
        'type': 'git',
        'url': url
    })
    print('Prepare mission {} from {}'.format(slug, url))


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
    verification_folder_path = folder.container_verification_folder_path()
    if os.path.exists(verification_folder_path):
        shutil.rmtree(verification_folder_path)

    copy_tree(folder.verification_folder_path(), verification_folder_path)
    docker.build(name_image=folder.image_name(), path=verification_folder_path)


def recompile_mission(slug):
    folder = Folder(slug)
    compiled_path = folder.compiled_folder_path()
    if os.path.exists(compiled_path):
        shutil.rmtree(compiled_path)

    mission_source = MissionFilesCompiler(compiled_path)
    mission_source.compile(source_path=folder.mission_folder(), use_link=True)
