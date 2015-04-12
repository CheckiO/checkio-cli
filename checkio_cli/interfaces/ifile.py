from checkio_cli.initial import get_file_options
from checkio_cli.testing import execute_referee
from checkio_cli.folder import Folder


def run(options):
    file_options = get_file_options(options.filename)
    folder = Folder(file_options['mission'])

    if not folder.exists():
        # TODO: try to get mission
        raise ValueError('Mission doesn\'t exists')

    if options.check:
        command = 'check'
    else:
        command = 'run'
    execute_referee(command, file_options['mission'], file_options['interpreter'],
                    without_container=options.without_container,
                    interface_child=options.interface_child,
                    interface_only=options.interface_only,
                    referee_only=options.referee_only)


def use(parser):
    parser.add_argument('filename')
    parser.add_argument('--check', action='store_true', default=False,
                        help='do check instead of simple run')
    parser.add_argument('--without-container', action='store_true', default=False,
                        help='start process without using container')
    parser.add_argument('--interface-child', action='store_true', default=False,
                        help='run interface as a child process')
    parser.add_argument('--interface-only', action='store_true', default=False,
                        help='out of two preocesses run interface only')
    parser.add_argument('--referee-only', action='store_true', default=False,
                        help='out of two preocesses run interface only')
    parser.set_defaults(func=run)
    return parser
