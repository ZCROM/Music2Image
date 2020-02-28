'''
Time Dependent Fourier Transform (Spectrogram)
Bryant Moquist
'''

import scipy
import numpy as np

def tdft(audio, srate, windowsize, windowshift,fftsize): #0.008, 0.004, 1024

    """Calculate the real valued fast Fourier transform of a segment of audio multiplied by a 
    a Hamming window.  Then, convert to decibels by multiplying by 20*log10.  Repeat for all
    segments of the audio."""
    
    windowsamp = int(windowsize*srate)
    shift = int(windowshift*srate)
    window = scipy.hamming(windowsamp)
    if type(np.dot(window, audio[0:0+windowsamp])) is np.ndarray:
        spectrogram = scipy.array([20*scipy.log10(abs(np.fft.rfft(np.dot(window, audio[i:i+windowsamp]), fftsize)))
                         for i in range(0, len(audio)-windowsamp, shift)])
    else:
        spectrogram = scipy.array([20 * scipy.log10(abs(np.fft.rfft(window * audio[i:i + windowsamp], fftsize)))
                                   for i in range(0, len(audio) - windowsamp, shift)])
    return spectrogram

