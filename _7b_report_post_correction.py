from pathlib import Path
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
from mri_distortion_toolkit.utilities import enumerate_subfolders
from _0_data_location import dataloc, scans
from scipy.spatial import Delaunay
from mri_distortion_toolkit.Reports import MRI_QA_Reporter
from mri_distortion_toolkit.utilities import plot_distortion_xyz_hist

from pathlib import Path


# extract markers uncorrected
try:
    # use existing segmentation if it exists
    volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm' / 'slicer_centroids.mrk.json')
except FileNotFoundError:
    # otherwise resegment
    volume = MarkerVolume(dataloc / scans['17'] / 'Original' / 'corrected_dcm',
                          n_markers_expected=609,
                          iterative_segmentation=True,
                          gaussian_image_filter_sd=.6)

    # note that we onlt expect 609 markers: we accidentally didn't capture the last slice of the phantom
    # with this scan
    print(f'for {scans["17"]}, {volume.MarkerCentroids.shape[0]} markers found')
    volume.export_to_slicer()
    volume.save_dicom_data()

# get matched volume for uncorrected
gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'
gt_vol = MarkerVolume(gt_data_loc)
# update coordinate system
gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'
gt_vol.rotate_markers(yaxis_angle=90)
gt_vol.rotate_markers(zaxis_angle=180)
gt_vol.rotate_markers(xaxis_angle=180)
rotated_match = MatchedMarkerVolumes(gt_vol, volume, n_refernce_markers=9)

# Direct data case: pass matched marker volume to MRI_QA_Reporter
# ---------------------------------------------------------------
# location to write reports:
user_home_dir = Path('~').expanduser()
report_dir = user_home_dir / 'mri_qa_reports'
if not report_dir.is_dir():
    report_dir.mkdir()
report = MRI_QA_Reporter(MatchedMarkerVolume=rotated_match.MatchedCentroids, r_outer=150, dicom_data=volume.dicom_data)
# report.write_html_report(report_name='post_correction_direct_data.html')