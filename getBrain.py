import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import threading
import multiprocessing
import utils  # Our own utility functions
from time import sleep
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

cred = credentials.Certificate('jaden-drone-firebase-adminsdk-54115-59e4733ce9.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jaden-drone.firebaseio.com'
})

def runBrain(arg):
    os.startfile('museTest.py')
    #Use os to run museTest and begin streaming muse data
x = threading.Thread(target=runBrain, args=(1,))
x.start()
#Create and start separate thread so that stream doesn't interfere with data retreival
ref = db.reference('/objRef')

chList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

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
#Set global variables


print('Looking for an EEG stream...')
streams = resolve_byprop('type', 'EEG', timeout=2)
#Look for eeg streams spawned from running museTest.py
if len(streams) == 0:
    #If no streams are found
    raise RuntimeError('Can\'t find EEG stream.')
    #Exception and message to user

print("Start acquiring data")
inlet = StreamInlet(streams[0], max_chunklen=12)
#Create an inlet to read data from first stream found
eeg_time_correction = inlet.time_correction()

info = inlet.info()
description = info.desc()
#Get info on stream inlet
fs = int(info.nominal_srate())


eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
print(eeg_buffer)
filter_state = None  # for use with the notch filter

n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                          SHIFT_LENGTH + 1))
band_buffer = np.zeros((n_win_test, 4))


if __name__ == '__main__':
    try:
        while True:
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))
            #Pull sample data from the stream inlet

            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
            #Create a numpy array of the data obtained

            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True,
                filter_state=filter_state)
            #Update eeg buffer with data pulled from inlet

            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)
            #Pull1 new row from the buffer array

            band_powers = utils.compute_band_powers(data_epoch, fs)
            #Break down eeg buffer into different frequency bands to distinguish between each individual signal measured
            #Every signal we want to measure(alpha, beta, theta, delta) has a specific frequency range with strict limits to each. By applying these limits, we can extract the specific values we want
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))
            #Update eeg buffer with new frequency bands

            #smooth_band_powers = np.mean(band_buffer, axis=0)

            delta_waves = band_powers[Band.Delta]
            theta_waves = band_powers[Band.Theta]
            alpha_waves = band_powers[Band.Alpha]
            beta_waves = band_powers[Band.Beta]
            #Extract wave amplitude for each band power measured
            strDet = str(alpha_waves)
            #Convert alpha wave amplitude float to string
            print("Alpha waves: " + strDet)
            #Print to user
            stMain = ""
            bn = 0
            while bn < len(strDet):
                #Loop through each character
                if strDet[bn] == ".":
                    #If decimal
                    stMain += "x"
                    #Add x to string as substitute
                elif strDet[bn] == "-":
                    #If float is negative
                    stMain += "-"
                    #Add it to str to indicate sign
                else:
                    #If character is numerical value between 0 and 9
                    stMain += chList[int(strDet[bn])]
                    #Use current character as index for chList to find corresponding alphabetical character
                bn += 1
            print(stMain)
            #Print string that represents alpha wave value
            reqStr = 'https://eduvh.herokuapp.com/' + stMain + '/brain'
            #Send to flask app by including in http request
            r=requests.get(reqStr)
            #Make http request to heroku server
    except KeyboardInterrupt:
        #If user exits
        print("   ")
        print("   ")
        print("Deads")
        print("   ")
        print("   ")
        print('Closing!')
        #Print message then terminate
