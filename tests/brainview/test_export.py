# Brainview unit tests for the export module.

import os
import pytest
import brainview as bv
import brainview.export as be
import numpy as np

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


def test_get_vertex_colors_no_adjust():
    morphometry_data = np.array([0.5, 0.1, 0.9])
    vertex_colors = be._get_vertex_colors(morphometry_data, 'viridis', -1)
    assert vertex_colors is not None
    assert vertex_colors.shape == (3, 4)
    assert vertex_colors[0][3] == 255


def test_get_vertex_colors_adjust_to_20():
    morphometry_data = np.array([0.5, 0.1, 0.9])
    vertex_colors = be._get_vertex_colors(morphometry_data, 'viridis', 20)
    assert vertex_colors is not None
    assert vertex_colors.shape == (3, 4)
    assert vertex_colors[0][3] == 20


def test_get_vertex_colors_no_colormap_given():
    morphometry_data = np.array([0.5, 0.1, 0.9])
    vertex_colors = be._get_vertex_colors(morphometry_data, None, 20)
    assert vertex_colors is None


def test_get_vertex_colors_no_morphometry_data_given():
    morphometry_data = np.array([0.5, 0.1, 0.9])
    vertex_colors = be._get_vertex_colors(None, 'viridis', 20)
    assert vertex_colors is None


def test_get_vertex_colors_no_morphometry_data_and_no_colormap_given():
    morphometry_data = np.array([0.5, 0.1, 0.9])
    vertex_colors = be._get_vertex_colors(None, None, 20)
    assert vertex_colors is None
    
