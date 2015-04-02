from folder import Folder

INITIAL_TEMPLATE = '''#!/usr/bin/env checkio-cli
# START-SYSNFO do not remove it
# Mission: {mission_slug}
# Source: {source_type}:{source_url}
# Interpreter: {interpreter}
# END-SYSNFO
{code}'''


def init_path_file(path, slug, interpreter):
    write_solution(slug, interpreter, path)


def init_home_file(slug, interpreter):
    folder = Folder(slug)
    write_solution(slug, interpreter, folder.solution_path())


def write_solution(slug, interpreter, solution_path):
    folder = Folder(slug)
    solution_fh = open(solution_path, 'w')
    config = folder.mission_config()

    solution_fh.write(INITIAL_TEMPLATE.format(
        mission_slug=slug,
        source_type=config['source_type'],
        source_url=config['source_url'],
        interpreter=interpreter,
        code=folder.initial_code(interpreter)
    ))
    solution_fh.close()
