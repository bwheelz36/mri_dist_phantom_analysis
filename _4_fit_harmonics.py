from mri_distortion_toolkit import calculate_harmonics
from pathlib import Path
import pandas as pd
from mri_distortion_toolkit.utilities import get_dicom_data
import numpy as np
from _0_data_location import dataloc, scans, data_csv_loc


gradient_n_order = 8
B_field_n_order = 8


FieldData = pd.read_csv(data_csv_loc / 'tra_Bfields.csv', index_col=0).squeeze("columns")
dicom_data_loc = Path(dataloc / scans['9'] / 'Original' / 'dicom_data.json')  # previosly saved from a MarkerVolume
dicom_data = get_dicom_data(dicom_data_loc)
gradient_strength = np.array(dicom_data['gradient_strength'])
normalisation_factor = [1 / gradient_strength[0], 1 / gradient_strength[1], 1 / gradient_strength[2],
                        1]  # this normalised gradient harmonics to 1mT/m
G_x_Harmonics, G_y_Harmonics, G_z_Harmonics, B0_Harmonics = calculate_harmonics(FieldData,
                                                                                n_order=[gradient_n_order,
                                                                                         gradient_n_order,
                                                                                         gradient_n_order,
                                                                                         B_field_n_order],
                                                                                scale=normalisation_factor)
# save for downstream analysis:
G_x_Harmonics.harmonics.to_csv(data_csv_loc / 'G_x_Harmonics_tra.csv')
G_y_Harmonics.harmonics.to_csv(data_csv_loc / 'G_y_Harmonics_tra.csv')
G_z_Harmonics.harmonics.to_csv(data_csv_loc / 'G_z_Harmonics_tra.csv')
if B0_Harmonics:  # None evaluates as False
    B0_Harmonics.harmonics.to_csv(data_csv_loc / 'B0_Harmonics_tra.csv')
# ======================================================================================================================

FieldData = pd.read_csv(data_csv_loc / 'sag_Bfields.csv', index_col=0).squeeze("columns")
dicom_data_loc = Path(dataloc / scans['12'] / 'Original' / 'dicom_data.json')  # previosly saved from a MarkerVolume
dicom_data = get_dicom_data(dicom_data_loc)
gradient_strength = np.array(dicom_data['gradient_strength'])
normalisation_factor = [1 / gradient_strength[0], 1 / gradient_strength[1], 1 / gradient_strength[2],
                        1]  # this normalised gradient harmonics to 1mT/m
G_x_Harmonics, G_y_Harmonics, G_z_Harmonics, B0_Harmonics = calculate_harmonics(FieldData,
                                                                                n_order=[gradient_n_order,
                                                                                         gradient_n_order,
                                                                                         gradient_n_order,
                                                                                         B_field_n_order],
                                                                                scale=normalisation_factor)

# save for downstream analysis:
G_x_Harmonics.harmonics.to_csv(data_csv_loc / 'G_x_Harmonics_sag.csv')
G_y_Harmonics.harmonics.to_csv(data_csv_loc / 'G_y_Harmonics_sag.csv')
G_z_Harmonics.harmonics.to_csv(data_csv_loc / 'G_z_Harmonics_sag.csv')
if B0_Harmonics:  # None evaluates as False
    B0_Harmonics.harmonics.to_csv(data_csv_loc / 'B0_Harmonics_sag.csv')
# ======================================================================================================================

FieldData = pd.read_csv(data_csv_loc / 'cor_Bfields.csv', index_col=0).squeeze("columns")
dicom_data_loc = Path(dataloc / scans['14'] / 'Original' / 'dicom_data.json')  # previosly saved from a MarkerVolume
dicom_data = get_dicom_data(dicom_data_loc)
gradient_strength = np.array(dicom_data['gradient_strength'])
normalisation_factor = [1 / gradient_strength[0], 1 / gradient_strength[1], 1 / gradient_strength[2],
                        1]  # this normalised gradient harmonics to 1mT/m
G_x_Harmonics, G_y_Harmonics, G_z_Harmonics, B0_Harmonics = calculate_harmonics(FieldData,
                                                                                n_order=[gradient_n_order,
                                                                                         gradient_n_order,
                                                                                         gradient_n_order,
                                                                                         B_field_n_order],
                                                                                scale=normalisation_factor)

# save for downstream analysis:
G_x_Harmonics.harmonics.to_csv(data_csv_loc / 'G_x_Harmonics_cor.csv')
G_y_Harmonics.harmonics.to_csv(data_csv_loc / 'G_y_Harmonics_cor.csv')
G_z_Harmonics.harmonics.to_csv(data_csv_loc / 'G_z_Harmonics_cor.csv')
if B0_Harmonics:  # None evaluates as False
    B0_Harmonics.harmonics.to_csv(data_csv_loc / 'B0_Harmonics_cor.csv')
