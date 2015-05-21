import yaml


class ConfigVerificationException(Exception):
    def __init__(self, file_path, name, description):
        self.name = name
        self.file_path = file_path
        self.description = description

    def __str__(self):
        return 'Config Error in {file_path}:{name} {description}'.format(
            name=self.name,
            file_path=self.file_path,
            description=self.description
        )


def read_config(file_path):
    try:
        fh = open(file_path)
    except IOError:
        return {}
    try:
        return yaml.load(fh)
    finally:
        fh.close()


def set_value(config, conf_name, answer):
    if config.user_config.get(conf_name) == answer:
        return config

    prev_answer = config.user_config.get(conf_name)
    config.user_config[conf_name] = answer

    write_config(config.CONFIG_FILE, config.user_config)
    try:
        return reload(config)
    except ConfigVerificationException:
        if prev_answer is None:
            config.user_config.pop(conf_name)
        else:
            config.user_config[conf_name] = prev_answer
        write_config(config.CONFIG_FILE, config.user_config)
        raise


def setter(config):
    def _set_value(name, value):
        set_value(config, name, value)
    return _set_value


def write_config(file_path, config):
    fh = open(file_path, 'w')
    yaml.dump(config, fh, default_flow_style=False)
    fh.close()


def interactive_configuration_process():
    def ask(config, question, default, conf_name):
        answer = raw_input(question +' [' + default + ']: ')
        if not answer:
            answer = default
        try:
            return set_value(config, conf_name, answer)
        except ConfigVerificationException as e:
            print('Error: ' + e.description)
            return ask(config, question, default, conf_name)

    print('Welcome to CheckiO Client Configuration')

    # can't be imported globaly because of recursive import
    import config
    import aconfig
    print('Configuration data will be stored in two files {} and {}'
          .format(config.CONFIG_FILE, aconfig.CONFIG_FILE))
    config = ask(config, 'Choose a main folder for CheckiO', config.FOLDER, 'main_folder')
    config = ask(config, 'Choose a folder for mission sources'
                         '(can be usefull for missions author)', config.MISSIONS_FOLDER,
                         'missions_folder')
    config = ask(config, 'Choose a folder for your solutios', config.SOLUTIONS_FOLDER,
                         'solutions_folder')

    available_interpreters = ','.join(config.INTERPRETERS.keys())
    aconfig = ask(aconfig, 'Choose a current interpreter (' + available_interpreters + ')',
                  aconfig.INTERPRETER, 'interpreter')
    print(config.FOLDER)
