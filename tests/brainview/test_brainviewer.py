# Tests for the brainviewer script.
#
# These tests require the pacakge `pytest-console-scripts` from PyPI.

def test_brainviewer_help(script_runner):
    ret = script_runner.run('brainviewer', '--help')
    assert ret.success
    # just for example, let's assume that foobar --version
    # should output 3.2.1
    assert 'usage' in ret.stdout
    assert ret.stderr == ''
