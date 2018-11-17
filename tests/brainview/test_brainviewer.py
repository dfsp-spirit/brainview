# Tests for the brainviewer script.
#
# These tests require the pacakge `pytest-console-scripts` from PyPI.

import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

def test_brainviewer_help(script_runner):
    ret = script_runner.run('brainviewer', '--help')
    assert ret.success
    assert 'usage' in ret.stdout
    assert 'View brain morphometry data' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_subject1_curv_white_both_native(script_runner):
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-m',  'curv', '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading data for subject' in ret.stdout
    assert 'measure curv of surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_subject1_area_white_both_native(script_runner):
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-m',  'area', '-s', 'pial', '--hemi', 'lh', '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading data for subject' in ret.stdout
    assert 'measure area of surface pial for hemisphere lh' in ret.stdout
    assert ret.stderr == ''
