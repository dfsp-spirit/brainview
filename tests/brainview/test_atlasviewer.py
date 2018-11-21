# Tests for the atlasviewer script.
#
# These tests require the package `pytest-console-scripts`.

import os
import pytest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

def test_atlasviewer_help(script_runner):
    ret = script_runner.run('atlasviewer', '--help')
    assert ret.success
    assert 'usage' in ret.stdout
    assert 'View brain label data or brain annotation' in ret.stdout
    assert ret.stderr == ''


def test_atlasviewer_label_cortex(script_runner):
    ret = script_runner.run('atlasviewer', 'subject1', 'label', 'cortex', '-d', TEST_DATA_DIR, '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading label cortex for subject subject1 from subjects dir' in ret.stdout
    assert 'displaying on surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''


def test_atlasviewer_label_cortex_nonverbose(script_runner):
    ret = script_runner.run('atlasviewer', 'subject1', 'label', 'cortex', '-d', TEST_DATA_DIR)
    assert ret.success
    assert not 'Verbosity' in ret.stdout
    assert not 'Loading label cortex for subject subject1 from subjects dir' in ret.stdout
    assert not 'displaying on surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''


def test_atlasviewer_annot_aparc(script_runner):
    ret = script_runner.run('atlasviewer', 'subject1', 'atlas', 'aparc', '-d', TEST_DATA_DIR, '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading atlas aparc for subject subject1 from subjects dir' in ret.stdout
    assert 'displaying on surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''


def test_atlasviewer_annot_aparc_nonverbose(script_runner):
    ret = script_runner.run('atlasviewer', 'subject1', 'atlas', 'aparc', '-d', TEST_DATA_DIR)
    assert ret.success
    assert not 'Verbosity' in ret.stdout
    assert not 'Loading atlas aparc for subject subject1 from subjects dir' in ret.stdout
    assert not 'displaying on surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''
