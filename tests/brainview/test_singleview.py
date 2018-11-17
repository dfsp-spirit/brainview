import os
import pytest
import numpy as np
import mayavi.mlab as mlab
import brainload as bl
import brainview as bv
import mayavi

mlab.options.offscreen = True

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, os.pardir, 'test_data')

# Respect the environment variable BRAINVIEW_TEST_DATA_DIR if it is set. If not, fall back to default.
TEST_DATA_DIR = os.getenv('BRAINVIEW_TEST_DATA_DIR', TEST_DATA_DIR)


def test_brainload_works_and_testdata_exists():
    vert_coords, faces, morphometry_data, meta_data = bl.subject('subject1', subjects_dir=TEST_DATA_DIR)
    assert len(meta_data) == 20


def test_brain_morphometry_view_gets_created():
    vert_coords, faces, morphometry_data, meta_data = bl.subject('subject1', subjects_dir=TEST_DATA_DIR)
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(800, 600))
    surface = bv.brain_morphometry_view(fig, vert_coords, faces, morphometry_data)
    assert type(fig) == mayavi.core.scene.Scene


def test_brain_label_view_gets_created():
    vert_coords, faces, morphometry_data, morphometry_meta_data = bl.subject('subject1', subjects_dir=TEST_DATA_DIR, load_morphometry_data=False)
    verts_in_label, label_meta_data = bl.label('subject1', TEST_DATA_DIR, 'cortex', meta_data=morphometry_meta_data)
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(800, 600))
    surface = bv.brain_label_view(fig, vert_coords, faces, verts_in_label)
    assert type(fig) == mayavi.core.scene.Scene


def test_brain_atlas_view_gets_created():
    vert_coords, faces, morphometry_data, morphometry_meta_data = bl.subject('subject1', subjects_dir=TEST_DATA_DIR, load_morphometry_data=False)
    vertex_labels, label_colors, label_names, atlas_meta_data = bl.annot('subject1', TEST_DATA_DIR, 'aparc')
    fig = mlab.figure(bgcolor=(0, 0, 0), size=(800, 600))
    surface = bv.brain_atlas_view(fig, vert_coords, faces, vertex_labels, label_colors, label_names)
    assert type(fig) == mayavi.core.scene.Scene
