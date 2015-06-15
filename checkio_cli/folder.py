import os
import yaml

from checkio_cli.config import settings


def get_file_content(file_path):
    fh = open(file_path)
    try:
        return fh.read()
    finally:
        fh.close()


class Folder(object):
    def __init__(self, slug):
        assert slug, 'incorect slug parameter for Folder'
        self.u_slug = slug
        self.f_slug = slug.replace('-', '_')

    def exists(self):
        return os.path.exists(self.mission_folder())

    def image_name(self):
        return 'checkio/' + self.u_slug

    def mission_folder(self):
        return os.path.join(settings.MISSIONS_FOLDER, self.f_slug)

    def mission_config_path(self):
        return os.path.join(self.mission_folder(), '.checkio_cli.yaml')

    def compiled_folder_path(self):
        return os.path.join(settings.COMPILED_FOLDER, self.f_slug)

    def container_compiled_folder_path(self):
        return os.path.join(settings.CONTAINER_COMPILED_FOLDER, self.f_slug)

    def verification_folder_path(self):
        return os.path.join(self.compiled_folder_path(), 'verification')

    def container_verification_folder_path(self):
        return os.path.join(self.container_compiled_folder_path(), 'verification')

    def referee_requirements(self):
        return os.path.join(self.verification_folder_path(), 'requirements.txt')

    def interface_cli_folder_path(self):
        return os.path.join(self.compiled_folder_path(), 'interfaces', 'checkio_cli')

    def interface_cli_main(self):
        return os.path.join(self.interface_cli_folder_path(), 'src', 'main.py')

    def interface_cli_requirements(self):
        return os.path.join(self.interface_cli_folder_path(), 'requirements.txt')

    def referee_folder_path(self):
        return os.path.join(self.verification_folder_path(), 'src')

    def envs_folder_path(self):
        return os.path.join(self.verification_folder_path(), 'envs')

    def compiled_referee_folder_path(self):
        return os.path.join(self.container_verification_folder_path(), 'src')

    def compiled_envs_folder_path(self):
        return os.path.join(self.container_verification_folder_path(), 'envs')

    def native_env_folder_path(self):
        return os.path.join(settings.NATIVE_ENV_FOLDER, self.f_slug)

    def native_env_bin(self, call):
        return os.path.join(self.native_env_folder_path(), 'bin', call)

    def mission_config_read(self):
        return get_file_content(self.mission_config_path())

    def compiled_info_folder_path(self):
        return os.path.join(self.compiled_folder_path(), 'info')

    def compiled_info_file_content(self, file_name):
        try:
            return get_file_content(os.path.join(self.compiled_info_folder_path(), file_name))
        except IOError:
            return ''

    def mission_config_write(self, source_data):
        fh = open(self.mission_config_path(), 'w')
        yaml.dump({'source': source_data}, fh, default_flow_style=False)
        fh.close()

    def mission_config(self):
        fh = open(self.mission_config_path())
        try:
            return yaml.load(fh)
        finally:
            fh.close()

    def init_file_path(self, interpreter):
        return os.path.join(self.compiled_folder_path(), 'initial', interpreter)

    def initial_code(self, interpreter):
        return get_file_content(self.init_file_path(interpreter))

    def solution_path(self):
        extension = settings.INTERPRETERS[settings.INTERPRETER]['extension']
        return os.path.join(settings.SOLUTIONS_FOLDER, self.f_slug + '.' + extension)

    def solution_code(self):
        return get_file_content(self.solution_path())
