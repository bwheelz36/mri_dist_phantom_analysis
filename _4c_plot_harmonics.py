"""
produce some bar plots of the harmonics for publication
"""
import pandas as pd
from matplotlib import pyplot as plt
from mri_distortion_toolkit.Harmonics import SphericalHarmonicFit
from _0_data_location import data_csv_loc
from pathlib import Path

save_figs = True
save_path = Path(r'C:\Users\bwhe3635\Dropbox (Sydney Uni)\abstracts,presentations etc\Publications\FirstAuthor\MRI_QA\Figures\harmonics')
if save_figs:
    assert save_path.is_dir()

# Gx_Harmonics:
G_x_data = pd.read_csv(data_csv_loc / 'Gx.csv', index_col=0).squeeze("columns")
Gx = SphericalHarmonicFit(G_x_data)
Gx.plot_harmonics_pk_pk(cut_off=.01, title='a) Gx harmonics', return_axs=False,
                        drop_dominant_harmonic=True, plot_percentage_of_dominant=True)
if save_figs:
    plt.savefig(save_path / 'Gx.pdf')
    plt.close('all')

# Gy_Harmonics
G_y_data = pd.read_csv(data_csv_loc / 'Gy.csv', index_col=0).squeeze("columns")
Gy = SphericalHarmonicFit(G_y_data)
Gy.plot_harmonics_pk_pk(cut_off=.01, title='b) Gy harmonics', return_axs=False,
                        drop_dominant_harmonic=True, plot_percentage_of_dominant=True)
if save_figs:
    plt.savefig(save_path / 'Gy.pdf')
    plt.close('all')

# Gz_Harmonics
G_z_data = pd.read_csv(data_csv_loc / 'Gz.csv', index_col=0).squeeze("columns")
Gz = SphericalHarmonicFit(G_z_data)
Gz.plot_harmonics_pk_pk(cut_off=.01, title="c) Gz harmonics", return_axs=False,
                        drop_dominant_harmonic=True, plot_percentage_of_dominant=True)
if save_figs:
    plt.savefig(save_path / 'Gz.pdf')
    plt.close('all')

# B0
B0_data = pd.read_csv(data_csv_loc / 'B0.csv', index_col=0).squeeze("columns")
B0 = SphericalHarmonicFit(B0_data, n_order=8)
B0.plot_harmonics_pk_pk(cut_off=.1, title='d) B0 harmonics', return_axs=False,
                        drop_dominant_harmonic=False, plot_percentage_of_dominant=False)
if save_figs:
    plt.savefig(save_path / 'B0.pdf')
    plt.close('all')