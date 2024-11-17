import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import time

def data_transform(data, fs=256):
    """
    Transform EEG data into different frequency bands and calculate average magnitudes.
    
    Args:
        data: numpy array of EEG data
        fs: sampling frequency in Hz, defaults to 256
    
    Returns:
        dict: average magnitudes for each frequency band
    """
    # Calculate FFT for each channel separately
    fft_data = np.fft.fft(data, axis=1)
    freqs = np.fft.fftfreq(data.shape[1], 1/fs)
    magnitudes = np.abs(fft_data)

    # Create masks for each frequency band
    delta_mask = (freqs >= 0.5) & (freqs <= 4)
    theta_mask = (freqs >= 4) & (freqs <= 8)
    alpha_mask = (freqs >= 8) & (freqs <= 13)
    beta_mask = (freqs >= 13) & (freqs <= 30)
    gamma_mask = (freqs >= 30) & (freqs <= 100)

    # Calculate average magnitudes for each band
    average_magnitudes = {}
    for band, mask in zip(['delta', 'theta', 'alpha', 'beta', 'gamma'],
                          [delta_mask, theta_mask, alpha_mask, beta_mask, gamma_mask]):
        band_magnitudes = magnitudes[:, mask]
        average_magnitudes[band] = np.mean(band_magnitudes, axis=1) if band_magnitudes.size > 0 else 0
        print(average_magnitudes[band])

    return average_magnitudes