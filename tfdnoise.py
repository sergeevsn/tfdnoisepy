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
    # Interpolation function for start times
    interp = interp1d(offsets_sparse, times_sparse, fill_value="extrapolate")

    # Scan headers of the input SEG-Y file
    print(f"Scanning headers of {input_file}...")
    gather_numbers = []
    offsets = []
    with segyio.open(input_file, strict=False) as f:
        for i in tqdm(range(f.tracecount)):
            gather_numbers.append(f.header[i][gather_start_byte])
            offsets.append(f.header[i][offset_start_byte])

    # Create a DataFrame to organize gather and offset data
    df = pd.DataFrame({"gather": gather_numbers, "offset": offsets})
    fold = df.groupby("gather")["offset"].nunique().max()
    print(f"Total {len(np.unique(gather_numbers))} gathers of maximum {fold} fold.")

    # Copy the input file to the output file
    print(f"Copying input file to {output_file}")
    shutil.copyfile(input_file, output_file)

    # If a difference file is specified, copy the input file to it as well
    if difference_file:
        shutil.copyfile(input_file, difference_file)

    # Filter gathers
    print("Filtering gathers...")
    start_time = time()
    with segyio.open(input_file, strict=False) as f1:
        sample_interval = f1.bin[segyio.BinField.Interval] / 1_000_000
        print(f"Sample interval from Binary Header is {sample_interval} seconds")

        with segyio.open(output_file, "r+", strict=False) as f2:
            with segyio.open(difference_file, "r+", strict=False) as f3:
                with tqdm(total=len(pd.unique(df["gather"])), desc="Filtering gathers") as pbar:
                    for i, g in enumerate(pd.unique(df["gather"])):
                        # Get trace indices and offsets for the current gather
                        trace_indices = df[df["gather"] == g].index
                        current_offsets = df[df["gather"] == g]["offset"].values
                        gather = np.array([f1.trace[j] for j in trace_indices])

                        # Calculate start times if required
                        start_times = None
                        if use_start_times:
                            start_times = interp(current_offsets)

                        # Apply TFD noise rejection filter
                        gather_filtered = tfd_noise_rejection(
                            gather,
                            n_samples_stft,
                            n_aperture_traces,
                            threshold_multiplier,
                            1 / sample_interval,
                            start_times,
                        )

                        # Write filtered traces to the output file
                        for trind, tr in enumerate(trace_indices):
                            f2.trace[tr] = gather_filtered[trind]

                        # Write difference traces to the difference file
                        for trind, tr in enumerate(trace_indices):
                            f3.trace[tr] = gather[trind] - gather_filtered[trind]

                        pbar.update(1)

    print(f"All done! Total filtering time is {time() - start_time:.2f} seconds")