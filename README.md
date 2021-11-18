# Linear-Predictive-Coding-of-Speech-Signals

Linear Predictive Coding of Speech Analysis works on a basic principle that sample can be approximated as **linear combination of past speech samples** and my minimizing the sum of squared differences over finite interval between the actual speech samples and the linearly predicted ones, a unique set of predictor coefficients can be determined.

This project uses one of the application of LPC-A. Here we can generate or load an audio, analyse the time domain specs, frequency domain specs, LPC envelope of each frames and compressing audio based on LPC.

## Pre-requisites
Make sure you have installed the following packages:

1) PyQt5: ```pip install PyQt5```

Uses: for building User Interface

2) numpy: ```pip install numpy```

Uses: for performing high end computations

3) matplotlib: ```pip install matplotlib```

Uses: for plotting various graphs

4) soundfile: ```pip install SoundFile```

Uses: for working with audio file (read, write etc)

5) librosa: ```pip install librosa```

Uses: for performing lpc analysis

6) scipy: ```pip install scipy```

Uses: for computing frequency spectrum, filtering etc
