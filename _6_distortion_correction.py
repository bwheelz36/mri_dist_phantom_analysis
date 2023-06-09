"""
in this script we will use the averaged harmonics to correct the phantom after it had
 been rotated 90 degrees. The rotation step serves to ensure that the marker positions
 we are trying to correct are independant of the positioned we used to fit the harmonics.

 The script is quite long because we demonstrate multiple correction cases: 2D only,
 3D, and 3D+B0
"""

from _0_data_location import dataloc, scans
from mri_distortion_toolkit.utilities import get_dicom_data
from mri_distortion_toolkit.DistortionCorrection import ImageDomainDistortionCorrector
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume
from pathlib import Path
import shutil

distorted_data_loc = dataloc / scans['17'] / 'Original'  # this is a 'rotated' acquisition

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
                                correct_through_plane=False,
                                correct_B0=False,
                                B0_direction=B0_direction)  # this is something we have to detemine for each scan with trial and error

GDC.correct_all_images()
save_loc = distorted_data_loc / 'corrected_dcm_2D'
try:
    shutil.rmtree(save_loc)
except FileNotFoundError:
    pass
GDC.save_all_images_as_dicom(save_loc=save_loc)  # saves as dicom which can be read into analysis packages.

GDC = ImageDomainDistortionCorrector(ImageDirectory=distorted_data_loc.resolve(),
                                gradient_harmonics=[Path('_data/Gx.csv').resolve(),
                                                    Path('_data/Gy.csv').resolve(),
                                                    Path('_data/Gz.csv').resolve()],
                                B0_harmonics=Path('_data/B0.csv').resolve(),
                                dicom_data=dicom_data,
                                ImExtension='dcm',
                                correct_through_plane=True,
                                correct_B0=False,
                                B0_direction=B0_direction)  # this is something we have to detemine for each scan with trial and error

GDC.correct_all_images()
save_loc = distorted_data_loc / 'corrected_dcm_3D'
try:
    shutil.rmtree(save_loc)
except FileNotFoundError:
    pass
GDC.save_all_images_as_dicom(save_loc=save_loc)  # saves as dicom which can be read into analysis packages.

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