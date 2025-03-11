import numpy as np
import matplotlib.pyplot as plt 
import segyio
from tfdparams import *

filenames = ['test_data/01_test_shots.sgy', 
             'test_data/02_test_shots_denoise.sgy', 
             'test_data/03_difference.sgy']
titles = ['ORIGINAL', 
          f'TFD: n_samples_stft={n_samples_stft}, n_aperture_traces={n_aperture_traces}, threshold_multiplier={threshold_multiplier}', 
          'DIFFERENCE']
start_trace = 664
end_trace = 1328
plot_size = (30, 7)

plt.figure(figsize=plot_size)
for i, fname in enumerate(filenames):
  
    with segyio.open(fname, strict=False) as f:
        data = np.array([f.trace[j] for j in np.arange(start_trace, end_trace)])
        plt.subplot(1, 3, i+1)
        plt.title(titles[i])
        if i == 0:
            vmin = np.percentile(data, 2)
            vmax = np.percentile(data, 98)
        plt.imshow(data.T, vmin=vmin, vmax=vmax, cmap='gray', aspect='auto')
        plt.title(titles[i])
plt.tight_layout()
plt.savefig(f'tfd_compare.png')
plt.close()
