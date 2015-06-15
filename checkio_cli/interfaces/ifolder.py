from argparse import OPTIONAL

from checkio_cli.config import settings, tools
from checkio_cli.configure import interactive_configuration_process
from checkio_cli.getters import mission_git_getter, rebuild_mission, recompile_mission,\
    rebuild_native, make_mission_from_template, mission_git_init, TemplateWasntFound,\
    MissionFolderExistsAlready

from checkio_cli.initial import init_path_file, init_home_file
from checkio_cli.testing import execute_referee


def use_config(parser):
    parser.add_argument('name', nargs=OPTIONAL)
    parser.add_argument('value', nargs=OPTIONAL)

    def run(options):
        if not options.name:
            return interactive_configuration_process()

        if options.value:
            tools.set_value(options.name, options.value)
        else:
            value = settings.get_value(options.name)
            print("Value is {}".format(value))

    parser.set_defaults(func=run)


def use_active(parser):
    parser.add_argument('mission', nargs=OPTIONAL)
    parser.add_argument('interpreter', nargs=OPTIONAL)

    def run(options):
        if options.mission is None:
            print('Mission: {}\nInterpreter: {}'.format(
                settings.MISSION, settings.INTERPRETER
            ))
        if options.mission != '-':
            tools.set_value('mission', options.mission)
        if options.interpreter:
            tools.set_value('interpreter', options.interpreter)

    parser.set_defaults(func=run)


def use_get_git(parser):
    parser.add_argument('url')
    # TODO: make slug parameter optional
    parser.add_argument('mission')
    parser.add_argument('--without-container', action='store_true', default=False,
                        help='start process without using container')

    def run(options):
        mission_git_getter(options.url, options.mission)
        recompile_mission(options.mission)
        if not options.without_container:
            rebuild_mission(options.mission)
        init_home_file(options.mission, settings.INTERPRETER)
        rebuild_native(options.mission)
        tools.set_value('mission', options.mission)
    parser.set_defaults(func=run)


def use_compile_mission(parser):
    parser.add_argument('mission', nargs=OPTIONAL)

    def run(options):
        if options.mission:
            tools.set_value('mission', options.mission)
        recompile_mission(options.mission)
        rebuild_native(options.mission)
    parser.set_defaults(func=run)


def use_build_mission(parser):
    parser.add_argument('mission', nargs=OPTIONAL)

    def run(options):
        if options.mission:
            tools.set_value('mission', options.mission)
        rebuild_mission(options.mission)
    parser.set_defaults(func=run)


def use_build_native_env(parser):
    parser.add_argument('mission', nargs=OPTIONAL)

    def run(options):
        if options.mission:
            tools.set_value('mission', options.mission)
        rebuild_native(options.mission)
    parser.set_defaults(func=run)


def use_init(parser):
    parser.add_argument('filename', nargs=OPTIONAL)
    parser.add_argument('mission', nargs=OPTIONAL)
    parser.add_argument('interpreter', nargs=OPTIONAL)

    def run(options):
        if options.filename is None:
            return init_home_file(settings.MISSION, settings.INTERPRETER)
        if '.' in options.filename:
            mission, interpreter = tools.set_mi(options.mission, options.interpreter)
            return init_path_file(options.filename, mission, interpreter)
        # --------------------mission-slug, ----interpreter-name
        mission, interpreter = tools.set_mi(options.filename, options.mission)
        return init_home_file(mission, interpreter)
    parser.set_defaults(func=run)


def use_referee(parser, command):
    parser.add_argument('mission', nargs=OPTIONAL, default=settings.MISSION)
    parser.add_argument('interpreter', nargs=OPTIONAL, default=settings.INTERPRETER)
    parser.add_argument('--without-container', action='store_true', default=False,
                        help='start process without using container')
    parser.add_argument('--interface-child', action='store_true', default=False,
                        help='run interface as a child process')
    parser.add_argument('--interface-only', action='store_true', default=False,
                        help='out of two preocesses run interface only')
    parser.add_argument('--referee-only', action='store_true', default=False,
                        help='out of two preocesses run interface only')

    def run(options, command=command):
        mission, interpreter = tools.set_mi(options.mission, options.interpreter)
        execute_referee(command, mission, interpreter,
                        without_container=options.without_container,
                        interface_child=options.interface_child,
                        interface_only=options.interface_only,
                        referee_only=options.referee_only)
    parser.set_defaults(func=run)


def use_create_mission(parser):
    parser.add_argument('mission')
    parser.add_argument('origin', nargs=OPTIONAL)
    parser.add_argument('--template', nargs=OPTIONAL, default='simpleio')
    parser.add_argument('--without-container', action='store_true', default=False,
                        help='start process without using container')

    def run(options):
        try:
            make_mission_from_template(options.mission, options.template)
        except TemplateWasntFound as e:
            print(e)
            return
        except MissionFolderExistsAlready as e:
            print(e)
            answer = raw_input('Would you like to remove this folder? y/n').strip().lower()
            if answer == 'n':
                return
            if answer in ['', 'y']:
                make_mission_from_template(options.mission, options.template, force_remove=True)

        if options.origin:
            mission_git_init(options.mission, options.origin)

        recompile_mission(options.mission)
        if not options.without_container:
            rebuild_mission(options.mission)
        init_home_file(options.mission, settings.INTERPRETER)
        rebuild_native(options.mission)
        tools.set_value('mission', options.mission)

    parser.set_defaults(func=run)


def use_git_link_mission(parser):
    parser.add_argument('mission')
    parser.add_argument('origin')

    def run(options):
        mission_git_init(options.mission, options.origin)
        tools.set_value('mission', options.mission)

    parser.set_defaults(func=run)


def use(parser):
    subparsers = parser.add_subparsers()
    use_create_mission(subparsers.add_parser('create-mission', help='Create mission folder'))
    use_git_link_mission(subparsers.add_parser('git-link-mission',
                                               help='Link a mission folder with'
                                                    ' git repository'))

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
    for name in ('run', 'check', 'battle'):
        use_referee(subparsers.add_parser(name, help='{} a solution from home folder'.format(name)),
                    name)
    parser.add_argument('--logging', action='store_true', default=False,
                        help='Input file this data for task')
    return parser
