## tfdnoise.py

STFT Median Thresholding Filter, based on FreeUSP TFDNoise uitility.
The filtering function itself is in tfd.py.

Uses SegyIO for file reading https://github.com/equinor/segyio

tqdm for progress https://github.com/tqdm/tqdm

FreeUSP Toolkit https://stuartschmitt.com/FreeUSP/

### Install
```bash
git clone https://github.com/sergeevsn/tfdnoisepy.git
cd find_geom_errors
python3 -m venv .venv
pip install -r requirements.txt
```

### Test run
```bash
python3 tfdnoise.py
python3 makepics.py
```