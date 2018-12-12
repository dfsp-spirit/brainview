# Brainview unit tests for the export module.

import os
import pytest
import brainview as bv
import brainview.export as be

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')


def test_mesh_export_format_from_filename_obj():
    format, matched = be._mesh_export_format_from_filename('file.obj')
    assert format == "obj"
    assert matched == True


def test_mesh_export_format_from_filename_obj_with_path():
    format, matched = be._mesh_export_format_from_filename('/tmp/file.obj')
    assert format == "obj"
    assert matched == True


def test_mesh_export_format_from_filename_ply():
    format, matched = be._mesh_export_format_from_filename('file.ply')
    assert format == "ply"
    assert matched == True

def test_mesh_export_format_from_filename_whatever():
    format, matched = be._mesh_export_format_from_filename('file.txt')
    assert format == "obj" # obj is the default
    assert matched == False
