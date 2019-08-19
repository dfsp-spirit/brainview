"""
Export functions for brainview.

These functions allow one to export brain meshes, e.g., for loading into standard 3D modeling software.
"""


import brainload as bl
import os
import matplotlib
import brainload.meshexport as me


def clip_data_at_percentiles(data, lower=5, upper=95):
    """
    Clip data at given percentiles.

    Clip data at given percentiles to remove extreme values. Computes the percentiles, then sets all values which are more extreme to the percentile values. Useful for plotting data that has some outliers, as these will otherwise have a large impact on the color map and thus the readability of the plot: all the values of interest will look extremely similar if there are outliers.

    Parameters
    ----------
    data: numpy 1D array
        The full data to be clipped.

    lower: int, optional
        Lower percentile, all values below this percentile will be clipped to the value at this percentile. Defaults to 5.

    upper: int, optional
        Upper percentile, all values above this percentile will be clipped to the value at this percentile. Defaults to 95.

    Returns
    -------
    numpy array
        The clipped data.

    Examples
    --------
    >>> clipped_data = clip_data_at_percentiles(raw_data)
    """
    return np.clip(data, np.percentile(data, lower), np.percentile(data, upper))


def export_mesh_to_file(filename, vertex_coords, faces, morphometry_data=None, colormap_name='viridis', colormap_adjust_alpha_to=-1, clip_data_perc=None):
    export_format, matched = _mesh_export_format_from_filename(filename)
    if clip_data_perc is not None:
        morphometry_data = clip_data_at_percentiles(morphometry_data, clip_data_perc[0], clip_data_perc[1])
    export_string = _get_export_string(export_format, vertex_coords, faces, morphometry_data, colormap_name, colormap_adjust_alpha_to)

    with open(filename, "w") as text_file:
        text_file.write(export_string)


def _get_export_string(export_format, vertex_coords, faces, morphometry_data, colormap_name, colormap_adjust_alpha_to):
    if export_format not in ('obj', 'ply'):
        raise ValueError("ERROR: export_format must be one of {'obj', 'ply'} but is '%s'." % export_format)

    if export_format == 'obj':
        return bl.mesh_to_obj(vertex_coords, faces)
    else:
        vertex_colors = _get_vertex_colors(morphometry_data, colormap_name, colormap_adjust_alpha_to)
        return bl.mesh_to_ply(vertex_coords, faces, vertex_colors=vertex_colors)


def _get_vertex_colors(morphometry_data, colormap_name, colormap_adjust_alpha_to):
    """
    Determine vertex colors based on the data.

    Determine vertex colors based on the data. Note that is can happen that None is returned if the data does not contain the information required to determine vertex colors.

    Returns
    -------
    numpy array or None
        The vertex colors. If a color array is returned, it has dimensions (n, 4) if the given morphometry_data had length n. The 4 values per data point represent an RGBA color.
    """
    if morphometry_data is None or colormap_name is None:
        return None
    else:
        vertex_colors = me.scalars_to_colors_matplotlib(morphometry_data, colormap_name)
        if colormap_adjust_alpha_to >= 0:
            vertex_colors[:,3] = colormap_adjust_alpha_to
        return vertex_colors



def _mesh_export_format_from_filename(filename):
    """
    Determine a mesh output format based on a file name.

    Determine a mesh output format based on a file name. This inspects the file extension.

    Parameters
    ----------
    filename: string
        A file name, may start with a full path. Examples: 'brain.obj' or '/home/myuser/export/brain.ply'. If the file extension is not a recognized extension for a supported format, the default format 'obj' is returned.

    Returns
    -------
    format: string
        A string defining a supported mesh output format. One of ('ply', 'obj').

    matched: Boolean
        Whether the file name ended with a known extension. If not, the returned format was chosen because it is the default format.
    """
    if filename.endswith('.ply'):
        return 'ply', True
    elif filename.endswith('.obj'):
        return 'obj', True
    else:
        return 'obj', False
