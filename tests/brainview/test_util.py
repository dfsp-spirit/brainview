import os
import pytest
import numpy as np
import mayavi.mlab as mlab
import brainload as bl
import brainview as bv
import brainview.util as ut
import mayavi

try:
    import configparser # Python 3
except:
    import ConfigParser as configparser     # Python 2

mlab.options.offscreen = True

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

# Respect the environment variable BRAINVIEW_TEST_DATA_DIR if it is set. If not, fall back to default.
TEST_DATA_DIR = os.getenv('BRAINVIEW_TEST_DATA_DIR', TEST_DATA_DIR)


def test_get_default_config_filename():
    cfg_file = bv.get_default_config_filename()
    assert '.brainviewrc' in cfg_file


def test_get_config():
    cfg = bv.get_config()
    assert cfg.has_section('figure') == True


def test_get_config_from_file():
    cfg_file = os.path.join(TEST_DATA_DIR, 'brainviewrc')
    cfg = ut.get_config_from_file(cfg_file)
    assert cfg.has_section('figure') == True
    assert cfg.getint('figure', 'width') == 900
    assert cfg.getint('figure', 'height') == 400


def test_get_config_from_file_raises_on_missing_file():
    missing_cfg_file = os.path.join(TEST_DATA_DIR, 'brainviewrc_not_there')
    with pytest.raises(ValueError) as exc_info:
        cfg = ut.get_config_from_file(missing_cfg_file)
    assert 'not_there' in str(exc_info.value)
