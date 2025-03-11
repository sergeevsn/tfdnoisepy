## tfdnoise.py

STFT Median Thresholding Filter, based on FreeUSP TFDNoise uitility.
The filtering function itself is in tfd.py.
Utility ```tfdnoise.py``` takes a SEG-Y file, filters out all gathers in it 
and stores result in SEG-Y file, making a difference SEG-Y file as well.
Parameters are stored in tfdparams.py
Utility makepics.py draws a comparison plot of these 3 SEG-Y files for specified trace numbers.

Uses SegyIO for file reading https://github.com/equinor/segyio

tqdm for progress https://github.com/tqdm/tqdm

FreeUSP Toolkit https://stuartschmitt.com/FreeUSP/

### Install
```bash
git clone https://github.com/sergeevsn/tfdnoisepy.git
cd tfdnoisepy
python3 -m venv .venv
pip install -r requirements.txt
```

### Test run
```bash
python3 tfdnoise.py
python3 makepics.py
```
