"""
In step _4_, we calculated harmonics for every field estimate. However, there are some field estimates we trust
more than others (more on htis below).
In this script, we combine and average our trusted estimates to produce the harmonics we will use in subequent steps.

Trusted Harmonics
-----------------

for each gradient harmonic we should have 2 estimates we trust; 1 frequency and 1 phase
this script takes the average of these two 'trusted estimates'

tra:
phase_encode_direction: y
freq_encode_direction: x

sag
phase_encode_direction: z
freq_encode_direction: y

cor
phase_encode_direction: x
freq_encode_direction: z
"""

import pandas as pd
from _0_data_location import data_csv_loc


# Gx_Harmonics:
G_x1 = pd.read_csv(data_csv_loc / 'G_x_Harmonics_tra.csv', index_col=0).squeeze("columns")
G_x2 = pd.read_csv(data_csv_loc / 'G_x_Harmonics_cor.csv', index_col=0).squeeze("columns")
G_x = (G_x1 + G_x2) / 2
G_x.to_csv('_data/Gx.csv')


# Gy_Harmonics
G_y1 = pd.read_csv(data_csv_loc / 'G_y_Harmonics_tra.csv', index_col=0).squeeze("columns")
G_y2 = pd.read_csv(data_csv_loc / 'G_y_Harmonics_sag.csv', index_col=0).squeeze("columns")
G_y = (G_y1 + G_y2) / 2
G_y.to_csv('_data/Gy.csv')


# Gz_Harmonics
G_z1 = pd.read_csv(data_csv_loc / 'G_z_Harmonics_sag.csv', index_col=0).squeeze("columns")
G_z2 = pd.read_csv(data_csv_loc / 'G_z_Harmonics_cor.csv', index_col=0).squeeze("columns")
G_z = (G_z1 + G_z2) / 2
G_z.to_csv('_data/Gz.csv')


# B0
B01 = pd.read_csv(data_csv_loc / 'B0_Harmonics_sag.csv', index_col=0).squeeze("columns")
B02 = pd.read_csv(data_csv_loc / 'B0_Harmonics_cor.csv', index_col=0).squeeze("columns")
B03 = pd.read_csv(data_csv_loc / 'B0_Harmonics_tra.csv', index_col=0).squeeze("columns")
G_x = (B01 + B02 + B03) / 3
B01.to_csv('_data/B0.csv')
