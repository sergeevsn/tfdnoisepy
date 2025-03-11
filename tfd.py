from scipy.signal import stft, istft
import numpy as np
from scipy.ndimage import median_filter

def next_power_of_two(n):
    """Returns the nearest power of two >= n"""
    return 1 << (n-1).bit_length()

def tfd_noise_rejection(data, n_samples_stft, trace_aperture, threshold_multiplier, sampling_frequency, start_times=None):
    n_traces, n_samples = data.shape

    # Compute STFT for the first trace to get time stamps
    f_first, t, Zxx_first = stft(
        data[0],
        fs=sampling_frequency,
        window='hann',
        nperseg=n_samples_stft,
        noverlap=n_samples_stft // 2,
        boundary='even',
        padded=True
    )
    stfts = [Zxx_first]

    n_samples_stft = next_power_of_two(n_samples_stft)

    if n_samples_stft >= data.shape[1]:
        print('Number of n_samples_stft must be smaller than trace length!')
        return None
    
    if trace_aperture >= data.shape[0]:
        print('Parameter trace_aperture must be smaller than number of traces!')
        return None

    # Compute STFT for the remaining traces
    for i in range(1, n_traces):
        _, _, Zxx = stft(
            data[i],
            fs=sampling_frequency,
            window='hann',
            nperseg=n_samples_stft,
            noverlap=n_samples_stft // 2,
            boundary='even',
            padded=True
        )
        stfts.append(Zxx)

    stft_array = np.stack(stfts, axis=0)  # Shape (n_traces, n_freq, n_time)
    amplitudes = np.abs(stft_array)
    phases = np.angle(stft_array)

    # Save the DC component
    dc_component = amplitudes[:, 0:1, :].copy()
    
    # Global median for threshold
    median_per_freq = np.median(amplitudes, axis=0)
    global_median = np.median(median_per_freq)
    threshold = global_median * threshold_multiplier

    # Create a mask for exceeding the threshold
    mask = amplitudes > threshold

    # Apply time constraint
    if start_times is not None:
        # Convert start_times to an array if it is a scalar
        if np.isscalar(start_times):
            start_times = np.full(n_traces, start_times)
        else:
            start_times = np.asarray(start_times)
            if len(start_times) != n_traces:
                raise ValueError("start_times must be a scalar or have length n_traces")

        # For each trace, determine the starting time frame
        for i in range(n_traces):
            start_time_i = start_times[i]
            # Find the index of the first time frame >= start_time_i
            start_frame_idx = np.searchsorted(t, start_time_i, side='left')
            # Disable filtering for frames before start_frame_idx
            mask[i, :, :start_frame_idx] = False

    # Median filtering
    median_filtered_amp = median_filter(amplitudes, 
                                      size=(2*trace_aperture+1, 1, 1),
                                      mode='nearest')

    # Restore the DC component
    median_filtered_amp[:, 0:1, :] = dc_component
    
    # Apply replacement based on the mask
    amplitudes[mask] = median_filtered_amp[mask]

    # Inverse transform
    filtered_data = np.zeros_like(data)
    for i in range(n_traces):
        _, x = istft(
            amplitudes[i] * np.exp(1j*phases[i]),
            fs=sampling_frequency,
            window='hann',
            nperseg=n_samples_stft,
            noverlap=n_samples_stft//2,
            boundary=True,
            time_axis=-1
        )
        filtered_data[i] = x[:n_samples]  # Truncate to the original length

    return filtered_data