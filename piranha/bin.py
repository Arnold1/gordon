import os
import sys
import argparse

import boto3
from botocore.client import ClientError
from termcolor import colored

from .core import Bootstrap, Project

__version__ = "0.0.1"


def main(argv=None):

    argv = (argv or sys.argv)[1:]

    parser = argparse.ArgumentParser(usage=("%(prog)s [build | apply | startproject | startapp]"))
    subparsers = parser.add_subparsers()

    def add_default_arguments(p):
        p.add_argument("--region",
                       dest="region",
                       type=str,
                       help="AWS region where this project should be applied")

    startproject_parser = subparsers.add_parser('startproject', description='Start a new project')
    add_default_arguments(startproject_parser)
    startproject_parser.set_defaults(cls=Bootstrap)
    startproject_parser.set_defaults(func="startproject")
    startproject_parser.add_argument("project_name",
                                     type=str,
                                     help="Name of the project.")

    startapp_parser = subparsers.add_parser('startapp', description='Start a new app')
    add_default_arguments(startapp_parser)
    startapp_parser.set_defaults(cls=Bootstrap)
    startapp_parser.set_defaults(func="startapp")
    startapp_parser.add_argument("app_name",
                                     type=str,
                                     help="Name of the application.")
    startapp_parser.add_argument("--runtime",
                                 dest="runtime",
                                 default='py',
                                 type=str,
                                 choices=('py', 'js'),
                                 help="App runtime")

    build_parser = subparsers.add_parser('build', description='Build')
    add_default_arguments(build_parser)
    build_parser.set_defaults(cls=Project)
    build_parser.set_defaults(func="build")

    apply_parser = subparsers.add_parser('apply', description='Build')
    add_default_arguments(apply_parser)
    apply_parser.set_defaults(cls=Project)
    apply_parser.set_defaults(func="apply")
    apply_parser.add_argument("-s", "--stage",
                            dest="stage",
                            type=str,
                            default='dev',
                            required=True,
                            help="Stage where to apply this project")

    options, args = parser.parse_known_args(argv)

    path = os.getcwd()
    piranha = options.cls(path=path, **vars(options))
    getattr(piranha, options.func)()

    return 0
