from checkio_cli.config.exceptions import ConfigVerificationException
from checkio_cli.config.tools import set_value

def ask(question, default, conf_name):
    answer = raw_input(question + ' [' + default + ']: ')
    if not answer:
        answer = default
    try:
        return set_value(conf_name, answer)
    except ConfigVerificationException as e:
        print('Error: ' + e.description)
        return ask(question, default, conf_name)


def console_interactive():
    from checkio_cli.config import settings
    print('Welcome to CheckiO Client Configuration')

    print('Configuration data will be stored in two files {} and {}'
          .format(settings.CONFIG_FILE, settings.CONFIG_FILE))
    settings = ask('Choose a main folder for CheckiO', settings.FOLDER, 'main_folder')
    settings = ask('Choose a folder for mission sources'
                   '(can be usefull for missions author)', settings.MISSIONS_FOLDER,
                   'missions_folder')
    settings = ask('Choose a folder for your solutios', settings.SOLUTIONS_FOLDER,
                   'solutions_folder')

    available_interpreters = ','.join(settings.INTERPRETERS.keys())
    settings = ask('Choose a current interpreter (' + available_interpreters + ')',
                   settings.INTERPRETER, 'interpreter')
    print(settings.FOLDER)
