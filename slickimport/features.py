__author__ = 'jcorbett'

from reporting import import_start, import_end
import slickqa
import os
import glob
import traceback
import yaml
import sys


def import_features(slick, path, onstart=import_start, onend=import_end, delete=False):
    """ Import any features from the path specified.

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
    features_to_import = glob.glob(os.path.join(projects_dir, '*', 'features', '*', 'feature.yaml'))
    features_count = len(features_to_import)
    for index, feature_yaml_path in enumerate(features_to_import):
        name = os.path.basename(os.path.dirname(feature_yaml_path))
        project_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(feature_yaml_path))))
        onstart('Component', name, index, features_count)
        try:
            info = dict()
            with open(feature_yaml_path, 'r') as yaml_file:
                info = yaml.load(yaml_file)
            if 'name' not in info:
                info['name'] = name
            feature = slickqa.Component.from_dict(info)
            existing = None
            try:
                existing = slick.projects(project_name).features(info['name']).get()
            except slickqa.SlickCommunicationError:
                pass
            if existing is not None:
                feature.id = existing.id
                slick.projects(project_name).features(feature).update()
            else:
                slick.projects(project_name).features(feature).create()
            if delete:
                os.unlink(feature_yaml_path)
        except:
            errors.append(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        onend('Component', name, index, features_count)

    return errors
