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
    temp = np.real(np.fft.ifft(fft_data * gamma_mask))
    sum = 0
    count = 0
    for row in temp:
        for element in row:
            if element != 0:
                sum += element
                count += 1
    filtered_data = {}
    print(sum/count)
    print("Sum: ", sum)
    print("Count: ", count)
    filtered_data['delta'] = sum/count

""""
    filtered_data = {
        'theta': np.real(np.fft.ifft(fft_data * theta_mask)),
        'alpha': np.real(np.fft.ifft(fft_data * alpha_mask)),
        'beta': np.real(np.fft.ifft(fft_data * beta_mask)),
        'gamma': np.real(np.fft.ifft(fft_data * gamma_mask))
    }
    
    return filtered_data

    """