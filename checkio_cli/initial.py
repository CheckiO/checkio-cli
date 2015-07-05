import yaml
import os
import stat
import sys
import logging

from checkio_cli.folder import Folder
from checkio_cli.config import settings
from checkio_cli.config.tools import set_mi

INITIAL_LINE = '#!/usr/bin/env checkio-cli'
LABEL_START_SYS_INFO = 'START-SYSNFO'
LABEL_END_SYS_INFO = 'END-SYSNFO'
LABEL_END_INFO = 'END-INFO'

PY3 = sys.version_info[0] == 3
if PY3:
    raw_input = input


def get_file_options(filename):
    fh = open(filename)
    config_line = ''
    reading_config = False
    reading_config_done = False
    file_ext = filename.split('.')[-1]
    interpreter = settings.EXTENSTIONS[file_ext]
    comment_prefix = settings.INTERPRETERS[interpreter]['inline_comment']
    for line in fh:
        if line.startswith(comment_prefix + LABEL_END_SYS_INFO):
            reading_config_done = True
            break
        if reading_config:
            config_line += line[2:]
        if line.startswith(comment_prefix + LABEL_START_SYS_INFO):
            reading_config = True
            continue
    if not reading_config_done:
        # TODO: use all data from parsed arguments
        raise ValueError('File without SYSINFO')
    return yaml.load(config_line)


def init_path_file(path, slug, interpreter):
    write_solution(slug, interpreter, path)


def init_home_file(slug, interpreter):
    folder = Folder(slug)
    if not os.path.exists(folder.init_file_path(interpreter)):
        available_list = folder.init_available_list()
        if not available_list:
            logging.warning('Do not support any language. Initials is empty.')
            return
        default = available_list[0]
        str_propose = '[{}]/{}'.format(default, '/'.join(available_list[1:]))
        answer = raw_input(('Mission "{}" doesn\'t support {}.' +
                            ' Please choose one out of available {}:').format(slug, interpreter,
                                                                              str_propose))
        answer = answer.strip()
        if not answer:
            answer = default

        _, interpreter = set_mi(interpreter=answer, do_raise=False)
        return init_home_file(slug, interpreter)

    write_solution(slug, interpreter, folder.solution_path())


def write_solution(slug, interpreter, solution_path):
    logging.info("Write a solution into %s for %s %s", solution_path, slug, interpreter)
    folder = Folder(slug)
    mission_config = folder.mission_config()
    comment_prefix = settings.INTERPRETERS[interpreter]['inline_comment']

    fh = open(solution_path, 'w')
    fh.write(INITIAL_LINE + '\n')
    fh.write(comment_prefix + LABEL_START_SYS_INFO + '\n')
    str_config = yaml.dump({
        'mission': slug,
        'source':  mission_config['source'],
        'interpreter': interpreter
    }, default_flow_style=False)
    for line in str_config.strip().split('\n'):
        fh.write(comment_prefix + line + '\n')
    fh.write(comment_prefix + LABEL_END_SYS_INFO + '\n')

    fh.write('\n')
    for file_name in settings.INIT_DESCRIPTION:
        for line in folder.compiled_info_file_content(file_name + '.md').split('\n'):
            if line.strip():
                fh.write(comment_prefix + line + '\n')
            else:
                # To avoid syntax warning 'trailing whitespace'
                fh.write(comment_prefix.strip() + '\n')
    fh.write(comment_prefix + LABEL_END_INFO + '\n\n')
    fh.write(folder.initial_code(interpreter))
    fh.close()

    st = os.stat(solution_path)
    os.chmod(solution_path, st.st_mode | stat.S_IEXEC)
