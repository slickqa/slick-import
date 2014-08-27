"""
This module holds the main method called by the slick-import utility.
"""

from __future__ import print_function

import os
import sys
import argparse
import pkg_resources

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='slick-import',
                                     description='Import and/or sync data into slick from a directory structure.  '
                                                 'For help with the layout of the directory structure take a look at: '
                                                 'http://github.com/slickqa/slick-import',
                                     version=pkg_resources.get_distribution('slickqa-slick-import').version)
    parser.add_argument('--delete', action='store_true', help='Delete files once their content is synced.')
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
