import numpy as np
import matplotlib.pyplot as plt 
import segyio
import shutil
from tqdm import tqdm
from scipy.interpolate import interp1d
import pandas as pd
from tfdparams import *
from tfd import tfd_noise_rejection
from time import time

if __name__ == "__main__":
    
    interp = interp1d(offsets_sparse, times_sparse, fill_value="extrapolate")

    print(f'Scanning headers of {input_file}...')
    gather_numbers = []
    offsets = []
    traces = []
    with segyio.open(input_file, strict=False) as f:
        for i in tqdm(range(f.tracecount)):
            gather_numbers.append(f.header[i][gather_start_byte])
            offsets.append(f.header[i][offset_start_byte])

    df = pd.DataFrame({'gather': gather_numbers, 'offset': offsets}) 
    fold = df.groupby('gather')['offset'].nunique().max()
    print(f'Total {len(np.unique(gather_numbers))} gathers of maximum {fold} fold.')

    print(f'Copying input file to {output_file}')
    shutil.copyfile(input_file, output_file)

    if difference_file:
        shutil.copyfile(input_file, difference_file)

    print('Filtering gathers...')
    start_time = time()
    with segyio.open(input_file, strict=False) as f1:
        sample_interval = f1.bin[segyio.BinField.Interval]/1000000
        print('Sample interval from Binary Header is ', sample_interval)
        with segyio.open(output_file, 'r+', strict=False) as f2:
            with segyio.open(difference_file, 'r+', strict=False) as f3:
                with tqdm(total=len(pd.unique(df['gather'])), desc="Filtering gathers") as pbar:
                    for i, g in enumerate(pd.unique(df['gather'])):
                    
                        trace_indices = df[df['gather'] == g].index
                        current_offsets = df[df['gather'] == g]['offset'].values
                        gather = np.array([f1.trace[j] for j in trace_indices]) 
                        start_times = None                 
                        if use_start_times:
                            start_times = interp(current_offsets)
                        
                        gather_filtered = tfd_noise_rejection(gather, n_samples_stft, n_aperture_traces, threshold_multiplier, 
                                                        1/sample_interval, start_times)
                

                        for trind, tr in enumerate(trace_indices):
                            f2.trace[tr] = gather_filtered[trind]
                        
                        for trind, tr in enumerate(trace_indices):
                            f3.trace[tr] = gather[trind] - gather_filtered[trind]    
                        pbar.update(1)

    print(f'All done! Total filtering time is {time() - start_time} seconds')


