# mri_dist_phantom_analysis

This repository demonstrates the anaysis of a distortion phantom using the [mri_distortion_toolkit](https://github.com/ACRF-Image-X-Institute/mri_distortion_toolkit).

The analysed was acquired on the australian MRI-Linac system, and can be downloaded [here](https://ses.library.usyd.edu.au/handle/2123/31139).

Upon downloading and unzipping the data, the first thing you should do is update the `dataloc` field in `_0_data_location.py`.
This variable should point to `20221107 MR Linac^Test` inside the downloaded data.

From here, you should be able to execute the scripts in order (_1_, _2_, etc.).
For explanation of what exactly is happening at each step, you can read our [documentation](https://acrf-image-x-institute.github.io/mri_distortion_toolkit/examples.html)

The only dependency you should need is `mri_distortion_toolkit`:

```commandline
pip install mri_distortion_toolkit
```