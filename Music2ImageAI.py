'''
Music Identification Program (a.k.a. Shazam/Soundhound)
Proof of Concept
Bryant Moquist
'''
# coding: utf-8

from __future__ import print_function
import scipy, pylab
from scipy.io.wavfile import read
import sys
import peakpicker as pp
import fingerprint as fhash
import matplotlib
import numpy as np
import tdft
import wave
import pylab as plt
import pandas as pd
# import load_vgg
# import utils
# import tensorflow as tf
from scipy.misc import imread, imresize
import random, shutil
from PIL import Image
import time

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

########################################## Music parameters ###################################################
CutTimeDef = 30  # Cut off file in 30s
interval = 10
#Song files to be hashed into database
# songs = []
songnames = []
numSongs = 0
dict = {}
separator = '.'

# TDFT parameters
windowsize = 0.008  # set the window size  (0.008s = 64 samples)
windowshift = 0.004  # set the window shift (0.004s = 32 samples)
fftsize = 1024  # set the fft size (if srate = 8000, 1024 --> 513 freq. bins separated by 7.797 Hz from 0 to 4000Hz)

# Peak picking dimensions
f_dim1 = 30
t_dim1 = 80
f_dim2 = 10
t_dim2 = 20
percentile = 70
base = 70  # lowest frequency bin used (peaks below are too common/not as useful for identification)
high_peak_threshold = 75
low_peak_threshold = 60

# Hash parameters
delay_time = 250  # 250*0.004 = 1 second
delta_time = 250 * 3  # 750*0.004 = 3 seconds
delta_freq = 128  # 128*7.797Hz = approx 1000Hz

# Time pair parameters
TPdelta_freq = 4
TPdelta_time = 2

#image
# imageGenre = []
# imageSamples = []
imageContentPath =[]
# imageStylePath = []

# analyze_audio_sample-------------------------------------------------------------------------
def AnalyzeAudio(filename, database, numSongs):
    # Audio sample to be analyzed and identified
    # print('Please enter an audio sample file to identify: ')
    userinput = filename
    sample = read(userinput)
    userinput = userinput.split(separator, 1)[0]

    print('Analyzing the audio sample: ' + str(userinput))
    srate = sample[0]  # sample rate in samples/second
    audio = sample[1]  # audio data
    spectrogram = tdft.tdft(audio, srate, windowsize, windowshift, fftsize)
    time = spectrogram.shape[0]
    freq = spectrogram.shape[1]

    # print('The size of the spectrogram is time: ' + str(time) + ' and freq: ' + str(freq))

    threshold = pp.find_thres(spectrogram, percentile, base)

    peaks = pp.peak_pick(spectrogram, f_dim1, t_dim1, f_dim2, t_dim2, threshold, base)

    # print('The initial number of peaks is:' + str(len(peaks)))
    peaks = pp.reduce_peaks(peaks, fftsize, high_peak_threshold, low_peak_threshold)
    # print('The reduced number of peaks is:' + str(len(peaks)))

    # Store information for the spectrogram graph
    samplePeaks = peaks
    sampleSpectro = spectrogram

    hashSample = fhash.hashSamplePeaks(peaks, delay_time, delta_time, delta_freq)
    # print('The dimensions of the hash matrix of the sample: ' + str(hashSample.shape))

    # print('Attempting to identify the sample audio clip.')
    timepairs = fhash.findTimePairs(database, hashSample, TPdelta_freq, TPdelta_time)
    # print(timepairs)

    # Compute number of matches by song id to determine a match

    songbins = np.zeros(numSongs)
    numOffsets = len(timepairs)
    offsets = np.zeros(numOffsets)
    index = 0
    for i in timepairs:
        offsets[index] = i[0] - i[1]
        index = index + 1
        songbins[int(i[2])] += 1

    # Identify the song
    print('The sample song is: ' + str(songnames[np.argmax(songbins)]))

    targetTracksId = songnames[np.argmax(songbins)][:-4]
    targetTracksId = str(int(targetTracksId))
    print('The sample song-genre is: ' + dict[targetTracksId])
    return dict[targetTracksId]    #str


def Music2Image(FileName):

    ###### setup()

    database = np.load('Fingerprint_HashMatrix.npy')
    with open('WavSongsNum.txt', 'r') as f:
        list1 = f.readlines()
    numSongs = len(list1)
    for i in range(0, len(list1)):
        list1[i] = list1[i].rstrip('\n')
        songnames.append(list1[i])

    # Read a tracks file
    with open("dealTracks.csv", "r", encoding="utf-8") as csvfile:
        dealTracks = pd.read_csv(csvfile)
        for i in range(len(dealTracks)):
            id = dealTracks.loc[i, ['track_id']]
            id = np.array(id)
            id = id.tolist()
            genre = dealTracks.loc[i, ['genre_top']]
            genre = np.array(genre)
            genre = genre.tolist()
            dict[str(id[0])] = genre[0]

    #----------------musicCut------------------------------------------
    imageContentPath.clear()

    Genre = "Folk"

    f = wave.open(r"" + FileName, "rb")
    params = f.getparams()
    # print(params)
    nchannels, sampwidth, framerate, nframes = params[:4]
    CutFrameNum = framerate * CutTimeDef
    str_data = f.readframes(nframes)
    f.close()

    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    temp_data = wave_data.T
    # StepNum = int(nframes/200)
    StepNum = CutFrameNum
    StepTotalNum = 0
    haha = 0

    # time_remaining = interval - time.time() % interval
    # time.sleep(time_remaining)
    styleImgFolderPath = "./ImageData/" + Genre + ".png"
    pic = Image.open(styleImgFolderPath)
    pic.show()

    while StepTotalNum < nframes:
        # for j in range(int(Cutnum)):
        print("Stemp=%d" % (haha))

        perFileName = "./musicCutResults/" + FileName[-6:-4] + "-" + str(haha + 1) + ".wav"
        temp_dataTemp = temp_data[StepNum * (haha):StepNum * (haha + 1)]
        haha = haha + 1
        StepTotalNum = haha * StepNum
        temp_dataTemp.shape = 1, -1
        temp_dataTemp = temp_dataTemp.astype(np.short)

        f = wave.open(perFileName, "wb")  # write wav files
        # 配置声道数、量化位数和取样频率
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        # 将wav_data转换为二进制数据写入文件
        f.writeframes(temp_dataTemp.tostring())
        f.close()

        # analyze_audio_sample-------------------------------------------------------------------------
        Genre = AnalyzeAudio(perFileName, database, numSongs)
        # time_remaining = interval - time.time() % interval
        # time.sleep(time_remaining)
        # content_img = imageContentPath[haha - 1]
        #
        styleImgFolderPath = "./ImageData/" + Genre + str(haha) + ".png"
        pic = Image.open(styleImgFolderPath)
        pic.show()


if __name__ == '__main__':
    FileName = './Music_input_data/RightHereWaiting.wav'
    Music2Image(FileName)