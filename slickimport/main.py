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
from configurations import import_configurations
from projects import import_projects
from components import import_components
from reporting import banner

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
    check_errors(import_configurations(slick, params.path[0], delete=params.delete))
    print(banner('Importing Projects'))
    check_errors(import_projects(slick, params.path[0], delete=params.delete))
    print(banner('Importing Components'))
    check_errors(import_components(slick, params.path[0], delete=params.delete))
    #print(banner('Importing Features'))
    #check_errors(import_features(slick, params.path[0], delete=params.delete))
    #print(banner('Importing Releases'))
    #check_errors(import_releases(slick, params.path[0], delete=params.delete))
    #print(banner('Importing Builds'))
    #check_errors(import_builds(slick, params.path[0], delete=params.delete))
    #print(banner('Importing Test Cases'))
    #check_errors(import_tests(slick, params.path[0], delete=params.delete))
    #print(banner('Importing Test Plans'))
    #check_errors(import_plans(slick, params.path[0], delete=params.delete))
    #print(banner('Importing Results'))
    #check_errors(import_results(slick, params.path[0], delete=params.delete))


