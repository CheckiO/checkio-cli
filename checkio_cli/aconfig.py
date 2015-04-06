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

if INTERPRETER not in config.INTERPRETERS:
    raise conf.ConfigVerificationException(CONFIG_FILE, 'interpreter', 'A wrong interpreter slug was choosen')