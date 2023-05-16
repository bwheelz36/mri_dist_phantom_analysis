import os
import logging
from pathlib import Path
import requests
import zipfile
from zipfile import BadZipFile

logging.basicConfig(level=logging.INFO)

def download_and_extract_data(dataloc):
    """ Function to facilitate downloading and extracting the Phantom data

    Args:
        dataloc (pathlib.Path): Path to the directory where the data will be downloaded and extracted to
    """
    zipfile_path = Path("./")
    data_zip_url = "https://ses.library.usyd.edu.au/bitstream/handle/2123/31139/mri_distortion_phantom_images.zip?sequence=1&isAllowed=y"
    with zipfile_path as dir:
        zip_file = Path(dir).joinpath("data.zip")

        if not dataloc.is_dir():
            logging.info("Downloading data zipfile...")
            data = requests.get(data_zip_url)

            logging.info("Extracting data zipfile...")
            with open(zip_file, 'wb') as out_file:
                out_file.write(data.content)
                try:
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        dir_to_extract_to = zipfile_path
                        zip_ref.extractall(dir_to_extract_to)
                except BadZipFile:
                    print("Cannot download data zipfile. Please confirm that the URL is valid.")
                    exit()
            logging.info("Data ready!")
        else:
            logging.info("Data already downloaded and extracted.")

dataloc = Path('./FrankenGoam^Mr/20221107 MR Linac^Test')
download_and_extract_data(dataloc)
if not dataloc.is_dir():
    raise NotADirectoryError(f'{dataloc} is not a directory')
scans = {'0': '01 localiser_gre',
         '1': '02 localiser_gre',
         '2': '03 localiser_gre',
         '3': '04 gre_trans_AP_330',
         '4': '05 gre_trans_PA_330',
         '5': '06 gre_sag_AP_330',
         '6': '07 gre_sag_PA_330',
         '7': '08 gre_cor_RL_330',
         '8': '09 gre_cor_LR_330',
         '9': '10 t1_tse_256_sag',
         '10': '11 t1_tse_256_sag_PA',
         '11': '12 t1_tse_256_tra_PA',
         '12': '13 t1_tse_256_sag_HF',
         '13': '14 t1_tse_256_sag_FH',  # for this one had to add gaussian_image_filter_sd=0.8
         '14': '15 t1_tse_256_cor_RL',
         '15': '16 t1_tse_256_cor_LR',
         '16': '17 localiser_gre',
         '17': '18 t1_tse_256_sag_HF_rot',
         '18': '19 t1_tse_256_sag_FH_rot',
         '19': '20 trufi_sag_128_torsocoil',
         '20': '21 trufi_sag_128_torsocoil',
         '21': '22 trufi_sag_128_torsocoil'}

# make a folder to store interim data in
this_file_loc = Path(__file__)
if not (this_file_loc.parent / '_data').is_dir():
    (this_file_loc.parent / '_data').mkdir()
# set variable to this location
this_file_loc = Path(__file__)
data_csv_loc = this_file_loc.parent / '_data'
