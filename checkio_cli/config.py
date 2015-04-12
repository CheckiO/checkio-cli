import os
import checkio_cli.configure as conf

USER_HOME = os.path.expanduser('~')
CONFIG_FILE = os.path.join(USER_HOME, '.checkio_cli.yaml')
ACTIVE_CONFIG_FILE = os.path.join(USER_HOME, '.active_checkio_cli.yaml')

user_config = conf.read_config(CONFIG_FILE)

# The FOLDER settings should go before start of first interactive configuration process
# because this is the first variable that will be writen
FOLDER = user_config.get('main_folder', os.path.join(USER_HOME, 'checkio'))

if not user_config:
    conf.interactive_configuration_process()
    user_config = conf.read_config(CONFIG_FILE)
active_user_config = conf.read_config(ACTIVE_CONFIG_FILE)

SOURCE_FOLDER = os.path.join(FOLDER, 'sources')
# for original mission repository
MISSIONS_FOLDER = user_config.get('missions_folder', os.path.join(SOURCE_FOLDER, 'missions'))
# for collected version with original
COMPILED_FOLDER = os.path.join(SOURCE_FOLDER, 'compiled')
# compailed folder contains same data but with resolved links
CONTAINER_COMPILED_FOLDER = os.path.join(SOURCE_FOLDER, 'container_compiled')
# for collecting native mosules
NATIVE_ENV_FOLDER = os.path.join(SOURCE_FOLDER, 'native')

SOLUTIONS_FOLDER = user_config.get('solutions_folder', os.path.join(FOLDER, 'solutions'))
# MD files that will be used in first user solution as well as initial user
INIT_DESCRIPTION = user_config.get('init_description', ['description', 'format_io'])

# Native run
NATIVE_PYTHON3 = 'python3'


INTERPRETERS = {
    'python_3': {'extension': 'py'},
    'python_2': {'extension': 'py'}
}

DOCKER_LINUX_IP = '172.17.42.1'
CONSOLE_SERVER_PORT = 7878

# TODO: default parameter for a parameter --without-container

import config
set_value = conf.setter(config)
