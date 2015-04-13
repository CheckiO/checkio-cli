import os
import configure as conf
import config

USER_HOME = os.path.expanduser('~')

CONFIG_FILE = os.path.join(USER_HOME, '.active_checkio_cli.yaml')
user_config = conf.read_config(CONFIG_FILE)

INTERPRETER = user_config.get('interpreter', 'python_3')
MISSION = user_config.get('mission')

import aconfig
set_value = conf.setter(aconfig)


def set_mi(mission=None, interpreter=None):
    if mission:
        set_value('mission', mission)
    else:
        mission = MISSION

    if interpreter:
        set_value('interpreter', interpreter)
    else:
        interpreter = INTERPRETER

    return mission, interpreter

if INTERPRETER not in config.INTERPRETERS:
    raise conf.ConfigVerificationException(CONFIG_FILE, 'interpreter',
                                           'A wrong interpreter slug was choosen')

if MISSION is not None:
    mission_folder = os.path.join(config.MISSIONS_FOLDER, MISSION.replace('-', '_'))
    if not os.path.exists(mission_folder):
        raise conf.ConfigVerificationException(CONFIG_FILE, 'interpreter',
                                               'A wrong mission name')
