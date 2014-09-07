__author__ = 'jcorbett'

import sys

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

def import_start(type, name, index, total):
    sys.stdout.write('* {} {} of {}: {}...'.format(type, index + 1, total, name))
    sys.stdout.flush()

def import_end(type, name, index, total):
    sys.stdout.write('done.\n')
    sys.stdout.flush()

