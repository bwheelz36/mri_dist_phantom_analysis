"""
this script demonstrates applying the distortion correction to a patient data set
"""

"""
in this script we will use the averaged harmonics to correct an independant dataset.
we will correct the phantom after it had been rotated 90 degrees
"""

from _0_data_location import dataloc, scans
from mri_distortion_toolkit.utilities import get_dicom_data
from mri_distortion_toolkit.DistortionCorrection import ImageDomainDistortionCorrector
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume
from pathlib import Path
from mri_distortion_toolkit.utilities import _get_MR_acquisition_data, dicom_to_numpy

distorted_data_loc = Path(r'C:\Users\bwhe3635\cloudstor\MRI-Linac Experimental Data\UQ PHANTOM^SHIMMING TEST\20210520 QA^QA\03 t2_tse_tra_fullphantom_z axis long')


InputVolume, dicom_affine, (X, Y, Z) = dicom_to_numpy(distorted_data_loc,
                                                      file_extension='dcm',
                                                      return_XYZ=True)
dicom_data = _get_MR_acquisition_data(distorted_data_loc, X, Y, Z)


GDC = ImageDomainDistortionCorrector(ImageDirectory=distorted_data_loc.resolve(),
                                gradient_harmonics=[Path('_data/Gx.csv').resolve(),
                                                    Path('_data/Gy.csv').resolve(),
                                                    Path('_data/Gz.csv').resolve()],
                                B0_harmonics=Path('_data/B0.csv').resolve(),
                                dicom_data=dicom_data,
                                ImExtension='dcm',
                                correct_through_plane=True,
                                correct_B0=True,
                                B0_direction='back')  # this is something we have to detemine for each scan with trial and error

GDC.correct_all_images()
save_loc = distorted_data_loc / 'corrected_dcm_3D_B0'
GDC.save_all_images_as_dicom(save_loc=save_loc)  # saves as dicom which can be read into analysis packages.
GDC.save_all_images()