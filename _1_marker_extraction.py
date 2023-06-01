"""
Automatically extracts the markers positions from each scan.
If the number of found markers is different from n_markers_expected, the software will warn you
Once extracted the markers are saved to a json file using the `export_to_slicer` command. As the
name implies, this file can be imported into slicer for further manipulation if required.
"""

from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume
from _0_data_location import dataloc, scans

# process TSE images
# this step can take a few minutes
scans_to_segment = ['9', '11', '12', '13', '14', '15']
gaussian_sd = [1, 1, 1, 0.8, 1, 1]
for scan, sd in zip(scans_to_segment, gaussian_sd):
    volume = MarkerVolume(dataloc / scans[scan] / 'Original', n_markers_expected=618, iterative_segmentation=True,
                          gaussian_image_filter_sd=sd)
    print(f'for {scans[scan]}, {volume.MarkerCentroids.shape[0]} markers found')
    volume.export_to_slicer()
    volume.save_dicom_data()