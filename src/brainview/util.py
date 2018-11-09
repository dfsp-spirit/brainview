"""
Utility functions for Brainview.
"""

import os
from ConfigParser import SafeConfigParser

def get_config():
    """
    Retrieve the brainload configuration.

    Tries to load the configuration from the default config file location. If that file does not exist, uses internal defaults.
    """
    default_config_file = get_default_config_filename()
    if os.path.isfile(default_config_file):
        return get_config_from_file(default_config_file)
    else:
        return get_default_config()


def write_default_config(config_file=None):
    """
    Write the default config to a config file in INI format.
    """
    if config_file is None:
        config_file = get_default_config_filename()
    config = get_default_config()
    with open(config_file, 'wb') as cf:
        config.write(cf)


def get_default_config_filename():
    return '.brainloadrc'


def get_config_from_file(settings_file):
    """
    Returns a config parsed from an INI. Currently, the file has to supply all required settings.
    """
    config = SafeConfigParser()
    config.read(settings_file)
    return config


def get_default_config():
    """
    Returns the default config.
    """
    config = SafeConfigParser()
    config.add_section('figure')
    config.set('figure', 'width', '800')
    config.set('figure', 'height', '600')
    return config
