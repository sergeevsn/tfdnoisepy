## tfdnoise.py

STFT Median Thresholding Filter, based on the FreeUSP TFDNoise utility. The filtering function itself is located in ```tfd.py```. The utility tfdnoise.py takes a SEG-Y file, filters all gathers within it, and stores the result in a new SEG-Y file, while also creating a difference SEG-Y file. Parameters for the filtering process are stored in ```tfdparams.py```. The utility ```makepics.py``` generates a comparison plot of these three SEG-Y files for specified trace numbers.

Uses ```SegyIO``` for file reading https://github.com/equinor/segyio

```tqdm``` for progress https://github.com/tqdm/tqdm

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
