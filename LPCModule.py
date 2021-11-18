'''
BACKEND CODE FOR LPC
main code: mainUI.py
created: Rajesh R, MS Research Scholar, IIT Mandi.
'''

import numpy as np
from scipy.signal.windows import hann, hamming
import math
from matplotlib import pyplot as plt
import soundfile as sf
import librosa as lb
from scipy import signal

'''
Function: Generates time domain plot
Parameters: path of input speech signal
Returns: time and amplitude of speech
'''
def timePlot(path):
    input_speech, fs = sf.read(path)
    n = np.arange(0, len(input_speech))
    y = input_speech
    return n, y

'''
Function: Creates frame blocks for short time processing
Parameters: speech input, window, overlap factor
Returns: seperated overlapped frames
'''
def FrameBlocks(sig, window, O=0.5):
    n = len(sig)
    nw = len(window)
    step = math.floor(nw * (1 - O))
    nb = math.floor((n - nw) / step) + 1
    frames = np.zeros((nb, nw))
    for i in range(nb):
        offset = i * step
        frames[i, :] = window * sig[offset: nw + offset]

    return frames

'''
Function: Calculates fft and LPC spectra of specific frames
Parameters: Speech input path, frame number, order of the filter
Returns: fft and lpc components for plotting
'''
def sprectrumvectors(path, frame_no, p=6):
    input_speech, fs = sf.read(path)
    sym = False
    wind = hamming(math.floor(0.03 * fs), sym)
    frames = FrameBlocks(input_speech, wind)

    frame = frames[frame_no]

    # LPC Spectrum
    a = lb.lpc(frame, p)
    b = 2
    w, h = signal.freqz(b, a)

    # FFT of frame
    fft_frame = np.log10(abs(np.fft.fft(frame)))
    fft_frame = fft_frame[:int(len(fft_frame) / 2)]
    x = np.arange(len(fft_frame))

    shift = np.mean(fft_frame)

    plt.plot(w / max(w), np.log10(abs(h)) + shift)
    plt.plot(x / max(x), fft_frame)

    x1 = w / max(w)
    y1 = np.log10(abs(h)) + shift
    x2 = x / max(x)
    y2 = fft_frame

    return x1, y1, x2, y2


'''
Function: Creates synthetic frames
Parameters: frames, LPC coefficients
Returns: synthetic frames
'''
def create_synthetic_frames(frames, coefficients):
    synthetic_frames = []
    poles = 1
    for frame in frames:
        residual = signal.lfilter(coefficients, poles, frame)
        synthetic = signal.lfilter([1], coefficients, residual)
        synthetic_frames.append(synthetic)

    return synthetic_frames

'''
Function: Performs overlap add of framed blocks into one speech signal
Parameters: frames, window, overlap factor
Returns: output speech
'''
def AddFrameBlocks(Blocks, window, O = 0.5):
    count, nw = Blocks.shape
    step = np.floor(nw * O)

    n = (count-1) * step + nw
    x = np.zeros((int(n), ))

    for i in range(count):
        offset = int(i * step)
        x[offset : nw + offset] += Blocks[i, :]

    return x

'''
Function: creates synthetic speech for UI purpose
Parameters: frame, lpc coefficient
Returns: synthetic signal
'''
def create_synthetic_frames2(frame, coefficients):
    poles = 1
    residual = signal.lfilter(coefficients, poles, frame)
    synthetic = signal.lfilter([1], coefficients, residual)
    return synthetic

'''
Function: main short time processing
Parameters: path of speech input
Returns: decoded%, path of output storage
'''
def shorttimeprocessing(path):
    input_speech, fs = sf.read(path)

    sym = False
    wind = hamming(math.floor(0.03 * fs), sym)
    frames = FrameBlocks(input_speech, wind)

    coefficients = []
    for frame in frames:
        coefficients.append(lb.lpc(frame, 16))

    # print(len(coefficients))

    synthetic_frames = []
    for i in range(0, len(frames)):
        synthetic_frames.append(create_synthetic_frames2(frames[i], coefficients[i]))

    reconstruted = AddFrameBlocks(np.array(synthetic_frames), wind)

    print('Data reduction by {}%'.format(len(input_speech) / len(reconstruted)))

    s = path.split('/')
    s.pop()
    a = s[0] + '/'
    k = a.join(s)

    sf.write(k + '/result.wav', reconstruted, fs)

    return len(input_speech)/len(reconstruted), k+'/result.wav'

'''
Function: UI Purpose, to calculate frame numbers
Parameters: path of speech input
Returns: length of frames
'''
def frameno(path):
    input_speech, fs = sf.read(path)
    sym = False
    wind = hamming(math.floor(0.03 * fs), sym)
    frames = FrameBlocks(input_speech, wind)
    return len(frames)

'''
Function: Generates new audio
Parameters: frequency, sampling frequency, sampling time
Returns: generated audio
'''
def generate_audio(f, fs, tsec):
    w = 2 * np.pi * f
    n = np.arange(0, fs * tsec, 1)
    y = np.cos(w * n)

    return y