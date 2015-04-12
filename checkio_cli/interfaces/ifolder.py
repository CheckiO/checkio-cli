from argparse import OPTIONAL, ONE_OR_MORE

from checkio_cli import config
from checkio_cli import aconfig
from checkio_cli.configure import interactive_configuration_process
from checkio_cli.getters import MISSION_GETTERS, rebuild_mission, recompile_mission, rebuild_native
from checkio_cli.initial import init_path_file, init_home_file
from checkio_cli.testing import execute_referee


def use_config(parser):
    parser.add_argument('name', nargs=OPTIONAL)
    parser.add_argument('value', nargs=OPTIONAL)

    def run(options):
        if not options.name:
            return interactive_configuration_process()

        if options.value:
            config.set_value(options.name, options.value)
        else:
            value = config.get_value(options.name)
            print("Value is {}".format(value))

    parser.set_defaults(func=run)


def use_active(parser):
    parser.add_argument('mission')
    parser.add_argument('interpreter', nargs=OPTIONAL)

    def run(options):
        if options.mission != '-':
            aconfig.set_value('mission', options.mission)
        if options.interpreter:
            aconfig.set_value('interpreter', options.interpreter)

    parser.set_defaults(func=run)


def use_get_git(parser):  # TODO: can be used by simple checkio-cli get
    parser.add_argument('url')
    parser.add_argument('slug')
    parser.add_argument('--without-container', action='store_true', default=False,
                        help='start process without using container')

    def run(options):
        MISSION_GETTERS['git'](options.url, options.slug)
        recompile_mission(options.slug)
        if not options.without_container:
            rebuild_mission(options.slug)
        init_home_file(options.slug, aconfig.INTERPRETER)
        rebuild_native(options.slug)
    parser.set_defaults(func=run)


def use_compile_mission(parser):
    parser.add_argument('slug')

    def run(options):
        recompile_mission(options.slug)
        rebuild_native(options.slug)
    parser.set_defaults(func=run)


def use_build_mission(parser):
    parser.add_argument('mission')

    def run(options):
        rebuild_mission(options.mission)
    parser.set_defaults(func=run)


def use_build_native_env(parser):
    parser.add_argument('mission')

    def run(options):
        rebuild_native(options.mission)
    parser.set_defaults(func=run)


def use_init(parser):
    parser.add_argument('filename', nargs=OPTIONAL)
    parser.add_argument('slug', nargs=OPTIONAL)
    parser.add_argument('interpreter', nargs=OPTIONAL)

    def run(options):
        if options.filename is None:
            return init_home_file()
        if '.' in options.filename:
            return init_path_file(options.filename, options.slug,
                                  options.interpreter or aconfig.INTERPRETER)
        # --------------------mission-slug, ----interpreter-name
        return init_home_file(options.filename, options.slug)
    parser.set_defaults(func=run)


def _use_referee(parser, command):
    parser.add_argument('mission', nargs=OPTIONAL, default=aconfig.MISSION)
    parser.add_argument('interpreter', nargs=OPTIONAL, default=aconfig.INTERPRETER)
    parser.add_argument('--without-container', action='store_true', default=False,
                        help='start process without using container')
    parser.add_argument('--interface-child', action='store_true', default=False,
                        help='run interface as a child process')
    parser.add_argument('--interface-only', action='store_true', default=False,
                        help='out of two preocesses run interface only')
    parser.add_argument('--referee-only', action='store_true', default=False,
                        help='out of two preocesses run interface only')

    def run(options, command=command):
        aconfig.set_mi(options.mission, options.interpreter)
        execute_referee(command, options.mission, options.interpreter,
                        without_container=options.without_container,
                        interface_child=options.interface_child,
                        interface_only=options.interface_only,
                        referee_only=options.referee_only)
    parser.set_defaults(func=run)


def use_check(parser):
    _use_referee(parser, 'check')


def use_run(parser):
    _use_referee(parser, 'run')


def use(parser):
    subparsers = parser.add_subparsers()
    use_config(subparsers.add_parser('config', help='Configure working folder'))
    use_active(subparsers.add_parser('active', help='Activate mission and interpreter'))

    use_get_git(subparsers.add_parser('get-git',
                                      help='Download and prepare mission from git-repo'))
    use_compile_mission(subparsers.add_parser('compile-mission',
                                              help='Collect all sources in one place'))
    use_build_mission(subparsers.add_parser('build-mission', help='Prepare a docker image'))
    use_build_native_env(subparsers.add_parser('build-native-env',
                                               help='Prepare a ENV for natove run'))

    use_init(subparsers.add_parser('init', help='Initial code'))
    use_check(subparsers.add_parser('check', help='Check a solution from home folder'))
    use_run(subparsers.add_parser('run', help='Run a code from a solution file'))
    parser.add_argument('--logging', action='store_true', default=False,
                        help='Input file this data for task')
    return parser
