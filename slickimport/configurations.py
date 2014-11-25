__author__ = 'jcorbett'

from reporting import import_start, import_end
import slickqa
import os
import glob
import traceback
import yaml
import sys

def import_configurations(slick, path, onstart=import_start, onend=import_end, delete=False):
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
            if delete:
                os.unlink(configuration_yaml_path)
        except:
            errors.append(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        onend('Configuration', name, index, configurations_count)
    return errors

