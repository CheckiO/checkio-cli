import os
import git
from distutils.dir_util import copy_tree

from checkio_cli.exceptions import ConfigException


class MissionFilesHandler(object):

    DIR_SOURCE = 'verification'

    SCHEMA_FILENAME = 'schema'

    DOCKER_TEMPLATE_FILENAME = 'Dockertemplate'
    DOCKER_ENV_FILENAME = 'Dockerenv'

    RUNNER_FILENAME = 'run.sh'

    def __init__(self, env, path, tmp_dir):
        self.env = env
        self.path = path
        self.config_execution = None
        self.config_base_repository = None
        self.path_destination = os.path.join(tmp_dir, 'checkio_mission')
        self.path_destination_source = os.path.join(self.path_destination, self.DIR_SOURCE)
        self.filepath_destination_runner = os.path.join(self.path_destination_source, 'envs',
                                                        self.RUNNER_FILENAME)

    def schema_parse(self):
        schema_file = os.path.join(self.path, self.DIR_SOURCE, self.SCHEMA_FILENAME)
        if not os.path.exists(schema_file):
            raise ConfigException('Config file does not exists.')

        with open(schema_file, 'r') as f:
            content = f.readline()
        if not content:
            raise ConfigException('Config file is empty')

        parts = content.split(';', 1)
        if len(parts) != 2:
            raise ConfigException('Config content is bad')
        self.config_execution = parts[0].strip()
        self.config_base_repository = parts[1].strip()

    def pull_base(self):
        try:
            git.Repo.clone_from(self.config_base_repository, self.path_destination)
        except git.GitCommandError as e:
            raise Exception(u"{}, {}".format(e or '', e.stderr))

    def copy_user_files(self):
        copy_tree(self.path, self.path_destination)

    def make_env_runner(self):
        runner_template = self._get_file_content(self.filepath_destination_runner)
        runner_template = runner_template.replace('{{env}}', self.env)
        with open(self.filepath_destination_runner, 'w') as f:
            f.write(runner_template)

    def make_dockerfile(self):
        docker_template_file = os.path.join(self.path_destination_source,
                                            self.DOCKER_TEMPLATE_FILENAME)
        docker_env_file = os.path.join(self.path_destination_source, 'envs', self.env,
                                       self.DOCKER_ENV_FILENAME)

        docker_template = self._get_file_content(docker_template_file)
        docker_env = self._get_file_content(docker_env_file)

        docker_template = docker_template.replace('{{env_instructions}}', docker_env)
        docker_template = docker_template.replace('{{env}}', self.env)

        with open(self.dockerfile, 'w') as f:
            f.write(docker_template)

    @property
    def dockerfile(self):
        return os.path.join(self.path_destination_source, 'Dockerfile')

    def _get_file_content(self, file):
        with open(file, "r") as file:
            return file.read()
