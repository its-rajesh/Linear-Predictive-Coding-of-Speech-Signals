# Linear-Predictive-Coding-of-Speech-Signals

Linear Predictive Coding of Speech Analysis works on a basic principle that sample can be approximated as **linear combination of past speech samples** and by minimizing the sum of squared differences over the finite interval between the actual speech samples and the linearly predicted ones, a unique set of predictor coefficients can be determined.

LPC Analysis widely used in estimating speech parameters such as pitch, formants, vocal tract, intensity (loudness) and provides extremely accurate results and selective speech computations

This project uses one of the applications of LPC-A. Here we can generate or load audio, analyze the time domain specs, frequency domain specs, LPC envelope of each frame, and compress audio based on LPC.

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

Uses: for computing frequency spectrum, filtering, etc

## Whats In?

- ```mainUI.py``` code comprises of UI components
- ```LPCModule.py``` is the backend with the core LPC analysis
- ```LPC.py``` has the LPC implementation without the UI
- ```should.wav``` and ```CantinaBand3.wav``` are few inputs to test the code
-  ```[Report.pdf](www.google.com)``` and ```LPC.ipynb``` contains the report for theory & explanation of codes
-  ```Usermanual.pdf``` contains how to use the UI

## Usage

```python mainUI.py```

## Author
> Rajesh R, MS Research Scholar, School of Computing & Electrical Engineering, Indian Institute of Technology, Mandi
>  
> Under Professor, Dr. Padmanabhan Rajan

> *Mail: S21005@students.iitmandi.ac.in*


