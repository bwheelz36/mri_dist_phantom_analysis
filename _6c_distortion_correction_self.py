"""
this illustrates the case of deriving harmonics from a dataset, and using those harmonics to correct the same data set
"""

"""
in this script we will use the averaged harmonics to correct an independant dataset.
we will correct the phantom after it had been rotated 90 degrees
"""

from _0_data_location import dataloc, scans
from mri_distortion_toolkit.utilities import get_dicom_data
from mri_distortion_toolkit.DistortionCorrection import ImageDomainDistortionCorrector
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
from pathlib import Path
import shutil

distorted_data_loc = dataloc / scans['11'] / 'Original'

try:
    dicom_data = get_dicom_data(distorted_data_loc / 'dicom_data.json')
except FileNotFoundError:
    volume = MarkerVolume(distorted_data_loc, ImExtension='dcm')
    volume.save_dicom_data()
    dicom_data = get_dicom_data(distorted_data_loc / 'dicom_data.json')

B0_direction = 'back'  # forward or back


GDC = ImageDomainDistortionCorrector(ImageDirectory=distorted_data_loc.resolve(),
                                gradient_harmonics=[Path('_data/Gx.csv').resolve(),
                                                    Path('_data/Gy.csv').resolve(),
                                                    Path('_data/Gz.csv').resolve()],
                                B0_harmonics=Path('_data/B0.csv').resolve(),
                                dicom_data=dicom_data,
                                ImExtension='dcm',
                                correct_through_plane=True,
                                correct_B0=True,
                                B0_direction=B0_direction)  # this is something we have to detemine for each scan with trial and error

GDC.correct_all_images()
save_loc = distorted_data_loc / 'corrected_dcm_3D_B0'
try:
    shutil.rmtree(save_loc)
except FileNotFoundError:
    pass
GDC.save_all_images_as_dicom(save_loc=save_loc)  # saves as dicom which can be read into analysis packages.

# get matched uncorrected_volume for uncorrected
gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'
gt_vol = MarkerVolume(gt_data_loc)
# update coordinate system
gt_vol.rotate_markers(yaxis_angle=180)  # rotate to put markers in same coordinate system

try:
    # use existing segmentation if it exists
    corrected_volume = MarkerVolume(
        dataloc / scans['11'] / 'Original' / 'corrected_dcm_3D_B0' / 'slicer_centroids.mrk.json')
except FileNotFoundError:
    # otherwise resegment
    corrected_volume = MarkerVolume(dataloc / scans['11'] / 'Original' / 'corrected_dcm_3D_B0',
                                      n_markers_expected=618,
                                      iterative_segmentation=True,
                                      gaussian_image_filter_sd=.6)
    print(f'for {scans["9"]}, {corrected_volume.MarkerCentroids.shape[0]} markers found')
    corrected_volume.export_to_slicer()
    corrected_volume.save_dicom_data()

matched_3D_B0 = MatchedMarkerVolumes(gt_vol, corrected_volume, n_refernce_markers=9)
matched_3D_B0.report()
elevation=28
azimuth=117
vmin = 0
vmax = 6
save_figs = True
save_path = Path(r'C:\Users\bwhe3635\Dropbox (Sydney Uni)\abstracts,presentations etc\Publications\FirstAuthor\MRI_QA\Figures\different_correction_techniques')
SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIGGER_SIZE = 18
matched_3D_B0.plot_3D_markers_with_color_scale(elevation=elevation, azimuth=azimuth,
                                            vmin=vmin, vmax=vmax, title='b) 2D correction',  return_axs=True)