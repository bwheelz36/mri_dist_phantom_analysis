from mri_distortion_toolkit.FieldCalculation import ConvertMatchedMarkersToBz
import pandas as pd
from pathlib import Path
from _0_data_location import dataloc, scans, data_csv_loc


# load the matched volume calculated in the previous step.
#transverse slices
matched_volume = pd.read_csv(data_csv_loc / 'tra_markers.csv', index_col=0).squeeze("columns")
dicom_data = dataloc / scans['9'] / 'Original' / 'dicom_data.json'  # previously saved from a MarkerVolume
Bz_field = ConvertMatchedMarkersToBz(matched_volume, dicom_data)
Bz_field.MagneticFields.to_csv(data_csv_loc / 'tra_Bfields.csv')

#sagital slices
matched_volume = pd.read_csv(data_csv_loc / 'sag_markers.csv', index_col=0).squeeze("columns")
dicom_data = dataloc / scans['12'] / 'Original' / 'dicom_data.json'  # previously saved from a MarkerVolume
Bz_field = ConvertMatchedMarkersToBz(matched_volume, dicom_data)
Bz_field.MagneticFields.to_csv(data_csv_loc / 'sag_Bfields.csv')

# coronal slices
matched_volume = pd.read_csv(data_csv_loc / 'cor_markers.csv', index_col=0).squeeze("columns")
dicom_data = dataloc / scans['14'] / 'Original' / 'dicom_data.json'  # previously saved from a MarkerVolume
Bz_field = ConvertMatchedMarkersToBz(matched_volume, dicom_data)
Bz_field.MagneticFields.to_csv(data_csv_loc / 'cor_Bfields.csv')


