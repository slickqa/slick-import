__author__ = 'jcorbett'

from reporting import import_start, import_end
import slickqa
import os
import glob
import traceback
import yaml
import sys


def import_projects(slick, path, onstart=import_start, onend=import_end, delete=False):
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
            if delete:
                os.unlink(project_yaml_path)
        except:
            errors.append(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        onend('Project', name, index, projects_count)

    return errors
