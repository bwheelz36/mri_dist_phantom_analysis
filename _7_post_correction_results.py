"""
Finally, we generate more matched marker volumes to generate reports of the distortion
post distortion correction in step _6_.
This script also produces the colored scatter plots presente in the paper.
"""

from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
from _0_data_location import dataloc, scans
from matplotlib import pyplot as plt
from pathlib import Path


process_original_data = True
process_2D_data = True
process_3D_data = True
process_3D_B0_data = True

# get matched uncorrected_volume for uncorrected
gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'
gt_vol = MarkerVolume(gt_data_loc)
# update coordinate system
gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'
gt_vol.rotate_markers(yaxis_angle=90)
gt_vol.rotate_markers(zaxis_angle=180)
gt_vol.rotate_markers(xaxis_angle=180)


if process_original_data:
    try:
        # use existing segmentation if it exists
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'slicer_centroids.mrk.json')
    except FileNotFoundError:
        # otherwise resegment
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original',
                              n_markers_expected=609,
                              iterative_segmentation=True,
                              gaussian_image_filter_sd=.6)
        # note that we onlt expect 609 markers: we accidentally didn't capture the last slice of the phantom
        # with this scan
        print(f'for {scans["17"]}, {uncorrected_volume.MarkerCentroids.shape[0]} markers found')
        uncorrected_volume.export_to_slicer()
        uncorrected_volume.save_dicom_data()
    original_matched = MatchedMarkerVolumes(gt_vol, uncorrected_volume, n_refernce_markers=9)

if process_2D_data:
    try:
        # use existing segmentation if it exists
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm_2D' / 'slicer_centroids.mrk.json')
    except FileNotFoundError:
        # otherwise resegment
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm_2D',
                              n_markers_expected=609,
                              iterative_segmentation=True,
                              gaussian_image_filter_sd=.6)
        print(f'for {scans["17"]}, {uncorrected_volume.MarkerCentroids.shape[0]} markers found')
        uncorrected_volume.export_to_slicer()
        uncorrected_volume.save_dicom_data()
    matched_2D = MatchedMarkerVolumes(gt_vol, uncorrected_volume, n_refernce_markers=9)

if process_3D_data:
    try:
        # use existing segmentation if it exists
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm_3D' / 'slicer_centroids.mrk.json')
    except FileNotFoundError:
        # otherwise resegment
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm_3D',
                              n_markers_expected=609,
                              iterative_segmentation=True,
                              gaussian_image_filter_sd=.6)
        print(f'for {scans["17"]}, {uncorrected_volume.MarkerCentroids.shape[0]} markers found')
        uncorrected_volume.export_to_slicer()
        uncorrected_volume.save_dicom_data()
    matched_3D = MatchedMarkerVolumes(gt_vol, uncorrected_volume, n_refernce_markers=9)

if process_3D_B0_data:
    try:
        # use existing segmentation if it exists
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm_3D_B0' / 'slicer_centroids.mrk.json')
    except FileNotFoundError:
        # otherwise resegment
        uncorrected_volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm_3D_B0',
                              n_markers_expected=609,
                              iterative_segmentation=True,
                              gaussian_image_filter_sd=.6)
        print(f'for {scans["17"]}, {uncorrected_volume.MarkerCentroids.shape[0]} markers found')
        uncorrected_volume.export_to_slicer()
        uncorrected_volume.save_dicom_data()
    matched_3D_B0 = MatchedMarkerVolumes(gt_vol, uncorrected_volume, n_refernce_markers=9)


# get convex hull of data covering initial data


volume_harmonics_calculated_in = MarkerVolume(dataloc / scans['9'] / 'Original' / 'slicer_centroids.mrk.json')
gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'
original_gt_vol = MarkerVolume(gt_data_loc)
original_gt_vol.rotate_markers(yaxis_angle=180)  # rotate to put markers in same coordinate system
matched_original = MatchedMarkerVolumes(original_gt_vol, volume_harmonics_calculated_in, n_refernce_markers=9)
XA = matched_original.MatchedCentroids[['x_gt', 'y_gt', 'z_gt']].to_numpy()

from scipy.spatial import Delaunay
import numpy as np
hull = Delaunay(XA)
keep_marker_ind = []
for marker in matched_3D_B0.MatchedCentroids.iterrows():
    XB = marker[1][4:7].to_numpy()
    is_in_data_hull = hull.find_simplex(XB) >= 0
    keep_marker_ind.append(is_in_data_hull)

from copy import deepcopy
matched_3D_B0_filtered = deepcopy(matched_3D_B0)
matched_3D_B0_filtered.MatchedCentroids = matched_3D_B0_filtered.MatchedCentroids[keep_marker_ind]



elevation=28
azimuth=117
vmin = 0
vmax = 6
cmap = plt.cm.rainbow
save_figs = True
save_path = Path(r'C:\Users\bwhe3635\Dropbox (Sydney Uni)\abstracts,presentations etc\Publications\FirstAuthor\MRI_QA\Figures\different_correction_techniques')
SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIGGER_SIZE = 18

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


if save_figs:
    assert save_path.is_dir()
original_matched.plot_3D_markers_with_color_scale(cmap=cmap, elevation=elevation, azimuth=azimuth,
                                                  vmin=vmin, vmax=vmax, title='a) No correction', return_axs=True)
plt.savefig(save_path / 'no_correction.pdf')
original_matched.report()
matched_2D.plot_3D_markers_with_color_scale(cmap=cmap, elevation=elevation, azimuth=azimuth,
                                            vmin=vmin, vmax=vmax, title='b) 2D correction',  return_axs=True)
plt.savefig(save_path / '2D_correction.pdf')
matched_2D.report()
matched_3D.plot_3D_markers_with_color_scale(cmap=cmap, elevation=elevation, azimuth=azimuth,
                                            vmin=vmin, vmax=vmax, title='c) 3D correction',  return_axs=True)
plt.savefig(save_path / '3D_correction.pdf')
matched_3D.report()
matched_3D_B0.plot_3D_markers_with_color_scale(cmap=cmap, elevation=elevation, azimuth=azimuth,
                                               vmin=vmin, vmax=vmax, title='D) 3D correction with B0',  return_axs=True)
plt.savefig(save_path / '3D_B0_correction.pdf')
matched_3D_B0_filtered.plot_3D_markers_with_color_scale(cmap=cmap, elevation=elevation, azimuth=azimuth,
                                                        vmin=vmin, vmax=vmax, title='d) 3D correction with B0 filtered',
                                                        return_axs=True)
plt.savefig(save_path / '3D_B0_correction_filtered.pdf')
matched_3D_B0.report()
matched_3D_B0_filtered.report()