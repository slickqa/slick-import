__author__ = 'jcorbett'

from reporting import import_start, import_end
import slickqa
import os
import glob
import traceback
import yaml
import sys


def import_components(slick, path, onstart=import_start, onend=import_end, delete=False):
    """ Import any components from the path specified.

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
    components_to_import = glob.glob(os.path.join(projects_dir, '*', 'components', '*', 'component.yaml'))
    components_count = len(components_to_import)
    for index, component_yaml_path in enumerate(components_to_import):
        name = os.path.basename(os.path.dirname(component_yaml_path))
        project_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(component_yaml_path))))
        onstart('Component', name, index, components_count)
        try:
            info = dict()
            with open(component_yaml_path, 'r') as yaml_file:
                info = yaml.load(yaml_file)
            if 'name' not in info:
                info['name'] = name
            component = slickqa.Component.from_dict(info)
            existing = None
            try:
                existing = slick.projects(project_name).components(info['name']).get()
            except slickqa.SlickCommunicationError:
                pass
            if existing is not None:
                component.id = existing.id
                slick.projects(project_name).components(component).update()
            else:
                slick.projects(project_name).components(component).create()
            if delete:
                os.unlink(component_yaml_path)
        except:
            errors.append(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        onend('Component', name, index, components_count)

    return errors
