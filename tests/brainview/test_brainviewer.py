# Tests for the brainviewer script.
#
# These tests require the package `pytest-console-scripts`.

import os
import pytest
import tempfile
import shutil

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


def test_brainviewer_subject1_area_pial_lh_native(script_runner):
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-m',  'area', '-s', 'pial', '--hemi', 'lh', '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading data for subject' in ret.stdout
    assert 'measure area of surface pial for hemisphere lh' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_subject1_area_pial_rh_native(script_runner):
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-m',  'area', '-s', 'pial', '--hemi', 'rh', '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading data for subject' in ret.stdout
    assert 'measure area of surface pial for hemisphere rh' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_nonverbose_subject1_area_white_both_native(script_runner):
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-m',  'area', '-s', 'pial', '--hemi', 'lh')
    assert ret.success
    assert not 'Verbosity' in ret.stdout
    assert not 'Loading data for subject' in ret.stdout
    assert not 'measure area of surface pial for hemisphere lh' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_common_fsaverage_subject1_area_white_both_native(script_runner):
    expected_fsaverage_surf_dir = os.path.join(TEST_DATA_DIR, 'fsaverage', 'surf')
    if not os.path.isdir(expected_fsaverage_surf_dir):
        pytest.skip("Test data missing: e.g., directory '%s' does not exist. You can get all test data by running './develop/get_test_data_all.bash' in the repo root." % expected_fsaverage_surf_dir)
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-c', '-f', '10', '-m',  'area', '-v')
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Loading data mapped to common subject fsaverage for subject subject1 from subjects dir' in ret.stdout
    assert 'measure area of surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_nonverbose_common_fsaverage_subject1_area_white_both_native(script_runner):
    expected_fsaverage_surf_dir = os.path.join(TEST_DATA_DIR, 'fsaverage', 'surf')
    if not os.path.isdir(expected_fsaverage_surf_dir):
        pytest.skip("Test data missing: e.g., directory '%s' does not exist. You can get all test data by running './develop/get_test_data_all.bash' in the repo root." % expected_fsaverage_surf_dir)
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-c', '-f', '10', '-m',  'area')
    assert ret.success
    assert not 'Verbosity' in ret.stdout
    assert not 'Loading data mapped to common subject fsaverage for subject subject1 from subjects dir' in ret.stdout
    assert not 'measure area of surface white for hemisphere both' in ret.stdout
    assert ret.stderr == ''


def test_brainviewer_export_mesh(script_runner):
    expected_fsaverage_surf_dir = os.path.join(TEST_DATA_DIR, 'fsaverage', 'surf')
    if not os.path.isdir(expected_fsaverage_surf_dir):
        pytest.skip("Test data missing: e.g., directory '%s' does not exist. You can get all test data by running './develop/get_test_data_all.bash' in the repo root." % expected_fsaverage_surf_dir)
    tmp_dir = os.path.join(tempfile.gettempdir(), '.{}'.format(hash(os.times())))
    os.makedirs(tmp_dir)
    export_file = os.path.join(tmp_dir, 'blah.obj')
    ret = script_runner.run('brainviewer', 'subject1' , '-d', TEST_DATA_DIR, '-c', '-f', '10', '-m',  'area', '-v', '-x', export_file)
    assert ret.success
    assert 'Verbosity' in ret.stdout
    assert 'Exporting brain mesh to file' in ret.stdout
    assert ret.stderr == ''
    shutil.rmtree(tmp_dir, ignore_errors=True)
