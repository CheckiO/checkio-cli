import yaml
import logging

try:
    from importlib import reload
except ImportError:
    pass

from checkio_cli.config.exceptions import ConfigVerificationException


def read_config(file_path):
    try:
        fh = open(file_path)
    except IOError:
        return {}
    try:
        conf_obj = yaml.load(fh)
        if not conf_obj:
            return {}
        return conf_obj
    finally:
        fh.close()


def set_value(conf_name, answer, do_raise=True):
    from checkio_cli.config import settings
    if settings.user_config.get(conf_name) == answer:
        return settings

    prev_answer = settings.user_config.get(conf_name)
    settings.user_config[conf_name] = answer

    write_config(settings.CONFIG_FILE, settings.user_config)
    try:
        return reload(settings)
    except ConfigVerificationException as e:
        if prev_answer is None:
            settings.user_config.pop(conf_name)
        else:
            settings.user_config[conf_name] = prev_answer
        write_config(settings.CONFIG_FILE, settings.user_config)
        if do_raise:
            raise
        else:
            logging.error(e.description)
            return None


def set_mi(mission=None, interpreter=None, do_raise=True):
    from checkio_cli.config import settings
    if mission:
        set_value('mission', mission, do_raise=do_raise)
    else:
        mission = settings.MISSION

    if interpreter:
        set_value('interpreter', interpreter, do_raise=do_raise)
    else:
        interpreter = settings.INTERPRETER

    return mission, interpreter


def setter(config_name):
    def _set_value(name, value):
        set_value(__import__(config_name), name, value)
    return _set_value


def write_config(file_path, config):
    fh = open(file_path, 'w')
    yaml.dump(config, fh, default_flow_style=False)
    fh.close()
