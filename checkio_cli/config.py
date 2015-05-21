import os
import checkio_cli.configure as conf

USER_HOME = os.path.expanduser('~')
CONFIG_FILE = os.path.join(USER_HOME, '.checkio_cli.yaml')
ACTIVE_CONFIG_FILE = os.path.join(USER_HOME, '.active_checkio_cli.yaml')
CLI_FOLDER = os.path.dirname(__file__)

user_config = conf.read_config(CONFIG_FILE)

# The FOLDER settings should go before start of first interactive configuration process
# because this is the first variable that will be writen
FOLDER = user_config.get('main_folder', os.path.join(USER_HOME, 'checkio'))

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

TEMPLATES_FOLDERS = [os.path.join(CLI_FOLDER, 'templates')]
if 'templates' in user_config:
    TEMPLATES_FOLDERS = user_config['templates'] + TEMPLATES_FOLDERS


INTERPRETERS = {
    'python_3': {'extension': 'py'},
    'python_2': {'extension': 'py'},
    'js_node': {'extension': 'js'}
}

DOCKER_LINUX_IP = '172.17.42.1'
CONSOLE_SERVER_PORT = 7878

# TODO: default parameter for a parameter --without-container

import config
set_value = conf.setter(config)

if user_config:
    for folder_name in (FOLDER, SOURCE_FOLDER, MISSIONS_FOLDER, COMPILED_FOLDER,
                        CONTAINER_COMPILED_FOLDER, NATIVE_ENV_FOLDER,
                        SOLUTIONS_FOLDER):
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
else:
    conf.interactive_configuration_process()
    # TODO: reimport the whole config file
    import sys
    sys.exit(0)
