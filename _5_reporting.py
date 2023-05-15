"""
produce a html report of the uncorrected gradient distortion using the averaged harmonics
"""

from mri_distortion_toolkit.Reports import MRI_QA_Reporter
import pandas as pd
from pathlib import Path
from _0_data_location import dataloc, scans


# location to write reports:
user_home_dir = Path('~').expanduser()
report_dir = user_home_dir / 'mri_qa_reports'
if not report_dir.is_dir():
    report_dir.mkdir()

# Harmonic case: pass harmonics to MRI_QA_Reporter so that data can be recontructed
# ----------------------------------------------------------------------------------
G_x_harmonics = pd.read_csv('_data/Gx.csv', index_col=0).squeeze("columns")
G_y_harmonics = pd.read_csv('_data/Gy.csv', index_col=0).squeeze("columns")
G_z_harmonics = pd.read_csv('_data/Gz.csv', index_col=0).squeeze("columns")
B0_harmonics  = pd.read_csv('_data/B0.csv', index_col=0).squeeze("columns")

dicom_data_loc = dataloc / scans['9'] / 'Original' / 'dicom_data.json'  # this supplies info about the scan type etc.

report = MRI_QA_Reporter(gradient_harmonics=[G_x_harmonics, G_y_harmonics, G_z_harmonics],
                         B0_harmonics=B0_harmonics,
                         r_outer=150, dicom_data=dicom_data_loc)

report.write_html_report(report_name='pre_correction_harmonics.html')