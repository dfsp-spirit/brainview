# Tests for the atlasviewer script.
#
# These tests require the package `pytest-console-scripts`.

import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

def test_atlasviewer_help(script_runner):
    ret = script_runner.run('atlasviewer', '--help')
    assert ret.success
    assert 'usage' in ret.stdout
    assert 'View brain label data or brain annotation' in ret.stdout
    assert ret.stderr == ''
