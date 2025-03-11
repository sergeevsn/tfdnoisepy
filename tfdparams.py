# File Parameters
input_file = 'test_data/test_shots.sgy'
output_file = 'test_data/test_shots_denoise.sgy'
difference_file = 'test_data/difference.sgy'

# SEG-Y Parameters
gather_start_byte = 9
offset_start_byte = 13

# TFD Parameters
n_samples_stft = 32
n_aperture_traces = 15
threshold_multiplier = 1.0

# Start time points
use_start_times = True
offsets_sparse = [0, 3350, 5000]                   
times_sparse  = [0.1, 0.9, 1.2]
