"""
In this script, we instead apply the distortion correction to a grid phantom.
The grid structure means it is much easier to visually assess distortion.

THis data set is not included with the rest of the data as it was a seperate acquisition; it
can be made available on request
"""
from mri_distortion_toolkit.DistortionCorrection import ImageDomainDistortionCorrector
from pathlib import Path
from mri_distortion_toolkit.utilities import _get_MR_acquisition_data, dicom_to_numpy

distorted_data_loc = Path(r'UQ PHANTOM^SHIMMING TEST\20210520 QA^QA\03 t2_tse_tra_fullphantom_z axis long')


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
GDC.save_all_images(DSV_radius=150)


