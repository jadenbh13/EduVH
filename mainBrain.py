import numpy as np  # Module that simplifies computations on matrices
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from twilio.rest import Client
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import threading
import multiprocessing
import utils  # Our own utility functions
import time
from pynput.keyboard import Key, Controller


delta_waves = 0
theta_waves = 0
alpha_waves = 0
beta_waves = 0

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


BUFFER_LENGTH = 5

EPOCH_LENGTH = 1

OVERLAP_LENGTH = 0.8

SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

INDEX_CHANNEL = [0]


print('Looking for an EEG stream...')
streams = resolve_byprop('type', 'EEG', timeout=2)
if len(streams) == 0:
    raise RuntimeError('Can\'t find EEG stream.')

print("Start acquiring data")
inlet = StreamInlet(streams[0], max_chunklen=12)
eeg_time_correction = inlet.time_correction()

info = inlet.info()
description = info.desc()
fs = int(info.nominal_srate())


eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
filter_state = None  # for use with the notch filter

n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                          SHIFT_LENGTH + 1))
band_buffer = np.zeros((n_win_test, 4))

print('Press Ctrl-C in the console to break the while loop.')

def dataStream():
    global delta_waves
    global alpha_waves
    global beta_waves
    global theta_waves

    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))

            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True,
                filter_state=filter_state)

            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)

            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))

            smooth_band_powers = np.mean(band_buffer, axis=0)

            delta_waves = band_powers[Band.Delta]
            theta_waves = band_powers[Band.Theta]
            alpha_waves = band_powers[Band.Alpha]
            beta_waves = band_powers[Band.Beta]

    except Exception as e:
        print(e)




if __name__ == '__main__':
    p = multiprocessing.Process(target=dataStream)
    p.start()
    try:
        while True:
            print('Delta: ', delta_waves, ' Theta: ', theta_waves,
                ' Alpha: ', alpha_waves, ' Beta: ', beta_waves)
            time.sleep(1)

    except KeyboardInterrupt:
        p.terminate()
