import sys
import os

from checkio_cli.folder import Folder


def use(parser):
    mission_slug = sys.argv[2]
    folder = Folder(mission_slug)
    os.system('cd {mission_path}; git {command}'.format(
        mission_path=folder.mission_folder(),
        command=' '.join(sys.argv[3:])
    ))
