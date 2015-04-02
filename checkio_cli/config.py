import os
CONFIG_FILE = '~/.checkio'

# TODO: get home folder
FOLDER = '/home/oduvan/checkio/'

SOURCE_FOLDER = os.path.join(FOLDER, 'sources')
# for original mission repository
MISSIONS_FOLDER = os.path.join(SOURCE_FOLDER, 'missions')
# for collected version with original
COMPILED_FOLDER = os.path.join(SOURCE_FOLDER, 'compiled')
# for collecting native mosules
NATIVE_ENV_FOLDER = os.path.join(SOURCE_FOLDER, 'native')

SOLUTIONS_FOLDER = os.path.join(FOLDER, 'solutions')

# Native run
NATIVE_PYTHON3 = 'python3'


ACTIVE_INTERPRETER = 'python_3'
ACTIVE_MISSION = 'test1'

INTERPRETERS = {
    'python_3': {'extension': 'py'},
    'python_2': {'extension': 'py'}
}

DOCKER_LINUX_IP = '172.17.42.1'
CONSOLE_SERVER_PORT = 7878

# TODO: reading and writing config file


# TODO
def set_value(name, value):
    print("Set config {} : {}".format(name, value))

# TODO
def get_value(name):
    return 'VALUE'


def get_mission_config(slug, value):
    'returns a config for current interpreter'
