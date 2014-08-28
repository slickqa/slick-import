"""
This module holds the main method called by the slick-import utility.
"""

from __future__ import print_function

import os
import sys
import argparse
import pkg_resources
import slickqa
import traceback
import glob
import yaml
import time

def banner(message, char='#', indent=4):
    """Return a banner of characters putting the message indented, surrounded
    :param message: The message to put in the characters
    :type message: str
    :param char: The character to repeat for the banner (1 character or it'll be too long)
    :type char: str
    :param indent: The number of characters to indent the message
    :type indent: int
    :return: a string containing the banner
    """
    return '{} {} {}'.format(char * indent, message, char * (80 - (indent + 2 + len(message))))


def check_errors(errors):
    if len(errors) > 0:
        for error in errors:
            print('ERROR: ', error)
        sys.exit(1)

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='slick-import',
                                     description='Import and/or sync data into slick from a directory structure.  '
                                                 'For help with the layout of the directory structure take a look at: '
                                                 'http://github.com/slickqa/slick-import',
                                     version=pkg_resources.get_distribution('slickqa-slick-import').version)
    parser.add_argument('--delete', action='store_true', help='Delete files once their content is synced.')
    parser.add_argument('-u', '--url', required=True, help='Base URL of slick, must be specified.')
    parser.add_argument('path', metavar='DIR', nargs=1, help='Path to the directory structure to import.')
    params = parser.parse_args(args)

    # validate arguments
    if not os.path.exists(params.path[0]):
        parser.print_usage(file=sys.stderr)
        print('ERROR: Invalid path "{}", path not found.\n'.format(params.path[0]), file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(params.path[0]):
        parser.print_usage(file=sys.stderr)
        print('ERROR: Invalid path "{}", path must be a directory.\n'.format(params.path[0]), file=sys.stderr)
        sys.exit(1)

    slick = None
    try:
        slick = slickqa.SlickConnection(params.url)
        version = slick.version.findOne()
        print('Connected to slick version "{}" at "{}".'.format(version.versionString, params.url))
    except slickqa.SlickCommunicationError:
        parser.print_usage(file=sys.stderr)
        print('ERROR: Unable to communicate with slick at URL: ', params.url, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    print(banner('Importing Configurations'))
    check_errors(import_configurations(slick, params.path[0]))
    print(banner('Importing Projects'))
    check_errors(import_projects(slick, params.path[0]))

def import_start(type, name, index, total):
    sys.stdout.write('* {}...'.format(name))
    sys.stdout.flush()

def import_end(type, name, index, total):
    sys.stdout.write('done.\n')
    sys.stdout.flush()

def import_configurations(slick, path, onstart=import_start, onend=import_end):
    """ Import any configurations from the path specified.

    :param slick: The connection to slick.
    :type slick: slickqa.SlickConnection
    :param path: The base path that contains the data to import
    :type path: str
    :param onstart: a function to be called when an import starts
    :type onstart: func
    :param onend: a function to be called when an import is finished
    :type onend: func
    :return: A list of errors (if any occured)
    """
    assert isinstance(slick, slickqa.SlickConnection)
    errors = []
    configuration_dir = os.path.join(path, 'configurations')
    if not os.path.exists(configuration_dir):
        return errors
    configurations_to_import = glob.glob(os.path.join(configuration_dir, '*.yaml'))
    configurations_count = len(configurations_to_import)
    for index, configuration_yaml_path in enumerate(configurations_to_import):
        name = os.path.basename(configuration_yaml_path)[:-5]
        onstart('Configuration', name, index, configurations_count)
        try:
            info = dict()
            with open(configuration_yaml_path, 'r') as yaml_file:
                info = yaml.load(yaml_file)
            if 'name' not in info:
                info['name'] = name
            config = slickqa.Configuration.from_dict(info)
            existing = slick.configurations.findOne(name=info['name'])
            if existing is not None:
                config.id = existing.id
                slick.configurations(config).update()
            else:
                slick.configurations(config).create()
        except:
            errors.append(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        onend('Configuration', name, index, configurations_count)
    return errors

def import_projects(slick, path, onstart=import_start, onend=import_end):
    """ Import any projects from the path specified.

    :param slick: The connection to slick.
    :type slick: slickqa.SlickConnection
    :param path: The base path that contains the data to import
    :type path: str
    :param onstart: a function to be called when an import starts
    :type onstart: func
    :param onend: a function to be called when an import is finished
    :type onend: func
    :return: A list of errors (if any occured)
    """
    assert isinstance(slick, slickqa.SlickConnection)
    errors = []
    projects_dir = os.path.join(path, 'projects')
    if not os.path.exists(projects_dir):
        return errors
    projects_to_import = glob.glob(os.path.join(projects_dir, '*', 'project.yaml'))
    projects_count = len(projects_to_import)
    for index, project_yaml_path in enumerate(projects_to_import):
        name = os.path.basename(os.path.dirname(project_yaml_path))
        onstart('Project', name, index, projects_count)
        try:
            info = dict()
            with open(project_yaml_path, 'r') as yaml_file:
                info = yaml.load(yaml_file)
            if 'name' not in info:
                info['name'] = name
            project = slickqa.Project.from_dict(info)
            existing = None
            try:
                existing = slick.projects(info['name']).get()
            except slickqa.SlickCommunicationError:
                pass
            if existing is not None:
                project.id = existing.id
                slick.projects(project).update()
            else:
                slick.projects(project).create()
        except:
            errors.append(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        onend('Project', name, index, projects_count)

    return errors
