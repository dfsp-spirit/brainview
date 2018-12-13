"""
Utility functions for Brainview.

Currently all of these are for configuration related stuff.
"""

import os
try:
    import configparser # Python 3
except:
    import ConfigParser as configparser     # Python 2

def get_config():
    """
    Retrieve the brainload configuration.

    Tries to load the configuration from the default config file location. If that file does not exist, uses internal defaults.

    Returns
    -------
    config: SafeConfigParser
        A config parser that contains Brainview configuration information. If the file `~/.brainloadrc` exists, the config gets loaded from that file. The file is expected to be in INI format. Otherwise, internal defaults settings are used. See get_default_config for available settings.

    config_file_used: string or None
        The path to the config file that was loaded, or None if the internal config was used.

    Examples
    --------
    Print the setting `width` from the section `figure` in the settings:

    >>> import brainview as bv
    >>> cfg, config_file_used = bv.get_config()
    >>> print cfg.getint('figure', 'width')
    800
    """
    default_config_file = get_default_config_filename()
    if os.path.isfile(default_config_file):
        return get_config_from_file(default_config_file), default_config_file
    else:
        return get_default_config(), None


def get_default_config_filename():
    """
    Return the path to the Brainview default config file.

    Return the path to the Brainview default config file. The file must be in INI format.

    Returns
    -------
    string
        The path to the Brainview default config file. This does not imply that the file exists.

    Examples
    --------
    >>> import brainview as bv
    >>> print bv.get_default_config_filename()
    /home/me/.brainloadrc
    """
    return os.path.join(os.getenv('HOME', ''), '.brainviewrc')


def get_config_from_file(ini_file):
    """
    Return the config parsed from the INI file.

    Return the config parsed from an INI file. Currently, the file has to supply all required settings.

    Parameters
    ----------
    ini_file: string
        Path to a configuration file in INI format.

    Returns
    -------
    configparser
        The configuration parsed from the ini_file.
    """
    if not os.path.isfile(ini_file):
        raise ValueError("Config file '%s' does not exist. Must be a readable file in INI format." % ini_file)
    config = configparser.ConfigParser()
    config.read(ini_file)
    return config


def get_default_config():
    """
    Return the default configuration.

    Return the default configuration that is stored internally (in the source code). Does not require access to the file system.

    Returns
    -------
    configparser
        The default configuration.
    """
    config = configparser.ConfigParser()
    config.add_section('figure')
    config.set('figure', 'width', '800')
    config.set('figure', 'height', '600')
    config.add_section('mesh')
    config.set('mesh', 'representation', 'surface') # see https://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html#triangular-mesh for representations
    config.set('mesh', 'colormap', 'cool') # the colormap to use for live mesh visualization in brainview, see https://docs.enthought.com/mayavi/mayavi/mlab.html#adding-color-or-size-variations for available maps
    config.add_section('meshexport')
    config.set('meshexport', 'colormap', 'viridis') # the colormap to use for mesh export when using vertex colors. This can use all matplotlib colormaps, see https://matplotlib.org/examples/color/colormaps_reference.html
    config.set('meshexport', 'colormap_adjust_alpha_to', '-1') # an integer value to set the alpha of the color values to when exporting (0..255). If set to any value < 0, the alpha values will not be changed.
    return config


def cfg_get(section, option, default_value, config=None):
    """
    Retrieve a string value from the configuration or use the default.

    Retrieve a string value from the configuration. If the config does not contain the value, use the default_value passed on a parameter instead.

    Parameters
    ----------
    section: string
        The section in the config that contains the requested option.

    option: string
        The requested option name. Its value in the configuration will be returned (if available).

    default_value: string
        The value to return if the configuration does not contain the requested data.

    config: configparser, optional.
        If given, the config is searched for the value. If omitted, this function will get the config itself, which may include loading it from disk. If you have already loaded the configuration, it is faster to pass it to prevent a useless reload.

    Returns
    -------
    string
        The option value. If the configuration contained the option in the requested section, the value is from the configuration. Otherwise, the parameter default_value is used.
    """
    return _cfg_get_any(section, option, default_value, 'string', config=config)


def cfg_getint(section, option, default_value, config=None):
    """
    Retrieve an int value from the configuration or use the default.

    Retrieve an int value from the configuration. If the config does not contain the value, use the default_value passed on a parameter instead.

    Parameters
    ----------
    section: string
        The section in the config that contains the requested option.

    option: string
        The requested option name. Its value in the configuration will be returned (if available).

    default_value: string
        The value to return if the configuration does not contain the requested data.

    config: configparser, optional.
        If given, the config is searched for the value. If omitted, this function will get the config itself, which may include loading it from disk. If you have already loaded the configuration, it is faster to pass it to prevent a useless reload.

    Returns
    -------
    int
        The option value. If the configuration contained the option in the requested section, the value is from the configuration. Otherwise, the parameter default_value is used.
    """
    return _cfg_get_any(section, option, default_value, 'int', config=config)


def cfg_getfloat(section, option, default_value, config=None):
    """
    Retrieve a float value from the configuration or use the default.

    Retrieve a float value from the configuration. If the config does not contain the value, use the default_value passed on a parameter instead.

    Parameters
    ----------
    section: string
        The section in the config that contains the requested option.

    option: string
        The requested option name. Its value in the configuration will be returned (if available).

    default_value: string
        The value to return if the configuration does not contain the requested data.

    config: configparser, optional.
        If given, the config is searched for the value. If omitted, this function will get the config itself, which may include loading it from disk. If you have already loaded the configuration, it is faster to pass it to prevent a useless reload.

    Returns
    -------
    float
        The option value. If the configuration contained the option in the requested section, the value is from the configuration. Otherwise, the parameter default_value is used.
    """
    return _cfg_get_any(section, option, default_value, 'float', config=config)


def cfg_getboolean(section, option, default_value, config=None):
    """
    Retrieve a Boolean value from the configuration or use the default.

    Retrieve a Boolean value from the configuration. If the config does not contain the value, use the default_value passed on a parameter instead.

    Parameters
    ----------
    section: string
        The section in the config that contains the requested option.

    option: string
        The requested option name. Its value in the configuration will be returned (if available).

    default_value: string
        The value to return if the configuration does not contain the requested data.

    config: configparser, optional.
        If given, the config is searched for the value. If omitted, this function will get the config itself, which may include loading it from disk. If you have already loaded the configuration, it is faster to pass it to prevent a useless reload.

    Returns
    -------
    boolean
        The option value. If the configuration contained the option in the requested section, the value is from the configuration. Otherwise, the parameter default_value is used.
    """
    return _cfg_get_any(section, option, default_value, 'boolean', config=config)



def _cfg_get_any(section, option, default_value, return_type, config=None):
    """
    Retrieve a value from the configuration or use the default.

    Retrieve a value from the configuration. If the config does not contain the value, use the default_value passed on a parameter instead.

    Parameters
    ----------
    section: string
        The section in the config that contains the requested option.

    option: string
        The requested option name. Its value in the configuration will be returned (if available).

    default_value: string
        The value to return if the configuration does not contain the requested data.

    return_type: one of ('string', 'int', 'float', 'boolean')

    config: configparser, optional.
        If given, the config is searched for the value. If omitted, this function will get the config itself, which may include loading it from disk. If you have already loaded the configuration, it is faster to pass it to prevent a useless reload.

    Returns
    -------
    option, type depends on return_type parameter
        The option value. If the configuration contained the option in the requested section, the value is from the configuration. Otherwise, the parameter default_value is used.
    """
    if return_type not in ('int', 'float', 'string', 'boolean'):
        raise ValueError("ERROR: return_type must be one of {'int', 'float', 'string', 'boolean'} but is '%s'." % return_type)

    if config is None:
        config, _ = get_config()
    if config.has_option(section, option):
        if return_type == 'int':
            return config.getint(section, option)
        elif return_type == 'float':
            return config.getfloat(section, option)
        elif return_type == 'boolean':
            return config.getboolean(section, option)
        else:
            return config.get(section, option)
    else:
        return default_value


def merge_two_dictionaries(dict1, dict2):
    """
    Merge two dictionaries.

    Merge two dictionaries, return the result. Does not alter the input dictionaries. Note that the order matters if the input dictionaries contain identical keys: the values from the second one will show up in the merged result.

    Parameters
    ----------
    dict1: dictionary
        The first dictionary.

    dict2: dictionary
        The second dictionary. Note that the order matters if the input dictionaries contain identical keys: the values from the second one will show up in the merged result.

    Returns
    -------
    dictionary
        The merged, new dictionary.
    """
    new_dict = dict1.copy()
    new_dict.update(dict2)
    return new_dict


def cfg_get_optional_values(section, option_dict, config=None):
    """
    Retrieve several configuration values ONLY if they are actually defined.

    Retrieve a dictionary of several configuration values ONLY if they are actually defined in the configuration.
    """
    result_dict= {}
    if config is None:
        config = get_config()
    for option, option_type in option_dict.items():
        if config.has_option(section, option):
            result_dict[option] = _cfg_get_any(section, option, None, option_type, config=config)
    return result_dict
