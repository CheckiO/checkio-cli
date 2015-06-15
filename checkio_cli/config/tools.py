import yaml
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
        return yaml.load(fh)
    finally:
        fh.close()


def set_value(conf_name, answer):
    from checkio_cli.config import settings
    if settings.user_config.get(conf_name) == answer:
        return settings

    prev_answer = settings.user_config.get(conf_name)
    settings.user_config[conf_name] = answer

    write_config(settings.CONFIG_FILE, settings.user_config)
    try:
        return reload(settings)
    except ConfigVerificationException:
        if prev_answer is None:
            settings.user_config.pop(conf_name)
        else:
            settings.user_config[conf_name] = prev_answer
        write_config(settings.CONFIG_FILE, settings.user_config)
        raise


def set_mi(mission=None, interpreter=None):
    from checkio_cli.config import settings
    if mission:
        set_value('mission', mission)
    else:
        mission = settings.MISSION

    if interpreter:
        set_value('interpreter', interpreter)
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
