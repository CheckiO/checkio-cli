import os

from checkio_cli.folder import Folder


def run(slug):
    folder = Folder(slug)
    print('Congratulation!!!')
    print('You have new mission created with slug {}'.format(slug))
    print('In the folder {} you find all files that explains what this mission about'
          .format(os.path.join(folder.mission_folder(), 'info')))
    print('Change initial user code in folder {}'
          .format(os.path.join(folder.mission_folder(), 'initial')))
