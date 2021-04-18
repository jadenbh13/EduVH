import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import threading
import utils  # Our own utility functions
from muselsl import stream, list_muses

BUFFER_LENGTH = 5

EPOCH_LENGTH = 1

OVERLAP_LENGTH = 0.8

SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

INDEX_CHANNEL = [0]
newVar = 8308

def indexs():
    indexer = newVar
    return indexer

try:
    # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
    while True:
        defe = indexs()
        print(defe)



except KeyboardInterrupt:
    print("   ")
    print("   ")
    print("Deads")
    print("   ")
    print("   ")
    print('Closing!')
