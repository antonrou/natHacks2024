import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import time

def data_transform(data, fs=256):
    """
    Transform EEG data into different frequency bands using FFT.
    
    Args:
        data: numpy array of EEG data
        fs: sampling frequency in Hz, defaults to 256
    
    Returns:
        dict: filtered data in different frequency bands
    """
    # Filter data into different frequency bands
    # Delta: 0.5-4 Hz
    delta_low = 0.5
    delta_high = 4
    
    # Theta: 4-8 Hz
    theta_low = 4
    theta_high = 8
    
    # Alpha: 8-13 Hz
    alpha_low = 8
    alpha_high = 13
    
    # Beta: 13-30 Hz
    beta_low = 13
    beta_high = 30
    
    # Gamma: 30-100 Hz
    gamma_low = 30
    gamma_high = 100
    
    # Calculate FFT
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data[0]), 1/fs)
    
    # Create masks for each frequency band
    delta_mask = (freqs >= delta_low) & (freqs <= delta_high)
    theta_mask = (freqs >= theta_low) & (freqs <= theta_high)
    alpha_mask = (freqs >= alpha_low) & (freqs <= alpha_high)
    beta_mask = (freqs >= beta_low) & (freqs <= beta_high)
    gamma_mask = (freqs >= gamma_low) & (freqs <= gamma_high)
    
    # Filter data for each band
    filtered_data = {}
    temp = freqs * delta_mask
    sum = 0
    count = 0
    for element in temp:
        if element != 0:
            sum += element
            count += 1
    filtered_data['delta'] = sum/count

    temp = freqs * gamma_mask
    sum = 0
    count = 0
    for element in temp:
        if element != 0:
            sum += element
            count += 1
    filtered_data['gamma'] = sum/count

    temp = freqs * theta_mask
    sum = 0
    count = 0
    for element in temp:
        if element != 0:
            sum += element
            count += 1
    filtered_data['theta'] = sum/count

    temp = freqs * alpha_mask
    sum = 0
    count = 0
    for element in temp:
        if element != 0:
            sum += element
            count += 1
    filtered_data['alpha'] = sum/count

    temp = freqs * beta_mask
    sum = 0
    count = 0
    for element in temp:
        if element != 0:
            sum += element
            count += 1
    filtered_data['beta'] = sum/count

    return filtered_data