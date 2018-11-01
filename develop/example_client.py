#!/usr/bin/env python
import os
import numpy as np
import brainload as bl
import mayavi.mlab as mlab
import brainview as bv


def run_example_client():
    subjects_dir = os.path.join(os.getenv('HOME'), 'data', 'tim_only')
    vert_coords, faces, morphometry_data, meta_data = bl.subject('tim', subjects_dir=subjects_dir)

    fig = mlab.figure(1, bgcolor=(0, 0, 0), size=(800, 600))
    brain = bv.singleview.get_brain_view(vert_coords, faces, morphometry_data)
    bv.singleview.show()


if __name__ == "__main__":
    run_example_client()
