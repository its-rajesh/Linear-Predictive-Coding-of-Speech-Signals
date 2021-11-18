import numpy as np
from scipy.signal.windows import hann, hamming
import math
from matplotlib import pyplot as plt
import soundfile as sf
import librosa as lb
import scipy
from scipy import signal


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




def plotLPC(frames, frame_no, p=6):
    frame = frames[frame_no]

    # LPC Spectrum
    a = lb.lpc(frame, p)
    b = 2
    w, h = signal.freqz(b, a)

    # FFT of frame
    fft_frame = np.log10(abs(np.fft.fft(frame)))
    fft_frame = fft_frame[:int(len(fft_frame) / 2)]
    x = np.arange(len(fft_frame))

    plt.title('Spectrum Analysis of frame: ' + str(frame_no))
    plt.xlabel('frequency in π units')
    plt.ylabel('log|X(w)|')

    shift = np.mean(fft_frame)
    #print(np.mean(fft_frame))

    plt.plot(w / max(w), np.log10(abs(h)) + shift)
    plt.plot(x / max(x), fft_frame)

    plt.legend(['LPC Envelope', 'DFT Spectrum'])
    #plt.savefig('/Users/rajeshr/Desktop/spect_analysis' + str(frame_no) + '.png')
    plt.show()

    return a


def create_synthetic_frames(frames, coefficients):
    synthetic_frames = []
    poles = 1
    for frame in frames:
        residual = signal.lfilter(coefficients, poles, frame)
        synthetic = signal.lfilter([1], coefficients, residual)
        synthetic_frames.append(synthetic)

    return synthetic_frames

def AddFrameBlocks(Blocks, window, O = 0.5):
    count, nw = Blocks.shape
    step = np.floor(nw * O)

    n = (count-1) * step + nw
    x = np.zeros((int(n), ))

    for i in range(count):
        offset = int(i * step)
        x[offset : nw + offset] += Blocks[i, :]

    return x

def shorttimeprocessing(path):
    input_speech, fs = sf.read(path)

    sym = False
    wind = hamming(math.floor(0.03 * fs), sym)
    frames = FrameBlocks(input_speech, wind)

    coefficients = plotLPC(frames, 15, 16)

    synthetic_frames = create_synthetic_frames(frames, coefficients)

    reconstruted = AddFrameBlocks(np.array(synthetic_frames), wind)

    print('Data reduction by {}%'.format(len(input_speech)/len(reconstruted)))

    s = path.split('/')
    s.pop()
    a = s[0] + '/'
    k = a.join(s)

    sf.write(k+'/reconstruted.wav', reconstruted, fs)



path = '/Users/rajeshr/Desktop/GeneratedAudio.wav'
shorttimeprocessing(path)