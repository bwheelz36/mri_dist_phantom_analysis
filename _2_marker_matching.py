"""
Match all distorted markers to the ground truth data
The matched marker datasets are saved to csv for future analysis
"""
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
from _0_data_location import dataloc, scans


gt_data_loc = dataloc.parent / 'CT' / 'slicer_centroids.mrk.json'

gt_vol = MarkerVolume(gt_data_loc)
gt_vol.rotate_markers(yaxis_angle=180)  # rotate to put markers in same coordinate system

# match transverse slice direction
tra_forward_vol = MarkerVolume(dataloc / scans['9'] / 'Original' / 'slicer_centroids.mrk.json')
tra_back_vol = MarkerVolume(dataloc / scans['11'] / 'Original' / 'slicer_centroids.mrk.json')
tra_match = MatchedMarkerVolumes(gt_vol, tra_forward_vol, reverse_gradient_data=tra_back_vol, n_refernce_markers=9)
tra_match.MatchedCentroids.to_csv('_data/tra_markers.csv')

# match sagital slice direction
sag_forward_vol = MarkerVolume(dataloc / scans['12'] / 'Original' / 'slicer_centroids.mrk.json')
sag_back_vol = MarkerVolume(dataloc / scans['13'] / 'Original' / 'slicer_centroids.mrk.json')
sag_match = MatchedMarkerVolumes(gt_vol, sag_forward_vol, reverse_gradient_data=sag_back_vol, n_refernce_markers=9)
sag_match.MatchedCentroids.to_csv('_data/sag_markers.csv')

# match coronal slice direction
cor_forward_vol = MarkerVolume(dataloc / scans['14'] / 'Original' / 'slicer_centroids.mrk.json')
cor_back_vol = MarkerVolume(dataloc / scans['15'] / 'Original' / 'slicer_centroids.mrk.json')
cor_match = MatchedMarkerVolumes(gt_vol, cor_forward_vol, reverse_gradient_data=cor_back_vol, n_refernce_markers=9)
cor_match.MatchedCentroids.to_csv('_data/cor_markers.csv')