import yaml
import os
import stat

from checkio_cli.folder import Folder
from checkio_cli.config import settings

INITIAL_LINE = '#!/usr/bin/env checkio-cli'
COMMENT_PREFIX = '# '
LABEL_START_SYS_INFO = 'START-SYSNFO'
LABEL_END_SYS_INFO = 'END-SYSNFO'
LABEL_END_INFO = 'END-INFO'


def get_file_options(filename):
    fh = open(filename)
    config_line = ''
    reading_config = False
    reading_config_done = False
    for line in fh:
        if line.startswith(COMMENT_PREFIX + LABEL_END_SYS_INFO):
            reading_config_done = True
            break
        if reading_config:
            config_line += line[2:]
        if line.startswith(COMMENT_PREFIX + LABEL_START_SYS_INFO):
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
    write_solution(slug, interpreter, folder.solution_path())


def write_solution(slug, interpreter, solution_path):
    folder = Folder(slug)
    mission_config = folder.mission_config()

    fh = open(solution_path, 'w')
    fh.write(INITIAL_LINE + '\n')
    fh.write(COMMENT_PREFIX + LABEL_START_SYS_INFO + '\n')
    str_config = yaml.dump({
        'mission': slug,
        'source':  mission_config['source'],
        'interpreter': interpreter
    }, default_flow_style=False)
    for line in str_config.strip().split('\n'):
        fh.write(COMMENT_PREFIX + line + '\n')
    fh.write(COMMENT_PREFIX + LABEL_END_SYS_INFO + '\n')

    fh.write('\n')
    for file_name in settings.INIT_DESCRIPTION:
        for line in folder.compiled_info_file_content(file_name + '.md').split('\n'):
            if line.strip():
                fh.write(COMMENT_PREFIX + line + '\n')
            else:
                # To avoid syntax warning 'trailing whitespace'
                fh.write(COMMENT_PREFIX.strip() + '\n')
    fh.write(COMMENT_PREFIX + LABEL_END_INFO + '\n\n')
    fh.write(folder.initial_code(interpreter))
    fh.close()

    st = os.stat(solution_path)
    os.chmod(solution_path, st.st_mode | stat.S_IEXEC)
