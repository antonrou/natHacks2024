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
    filtered_data = {
        'delta': np.real(np.fft.ifft(fft_data * delta_mask)),
        'theta': np.real(np.fft.ifft(fft_data * theta_mask)),
        'alpha': np.real(np.fft.ifft(fft_data * alpha_mask)),
        'beta': np.real(np.fft.ifft(fft_data * beta_mask)),
        'gamma': np.real(np.fft.ifft(fft_data * gamma_mask))
    }
    
    return filtered_data


def data_transform_realtime(data_stream, n_seconds=10, threshold=0.5):

    plt.ion()  # Turn on interactive mode for real-time plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    while True:
        # Get the latest chunk of data
        data = data_stream.get_next_chunk(chunk_size)
        
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
        filtered_data = {
            'delta': np.real(np.fft.ifft(fft_data * delta_mask)),
            'theta': np.real(np.fft.ifft(fft_data * theta_mask)),
            'alpha': np.real(np.fft.ifft(fft_data * alpha_mask)),
            'beta': np.real(np.fft.ifft(fft_data * beta_mask)),
            'gamma': np.real(np.fft.ifft(fft_data * gamma_mask))
        }
        
        # Use first channel of EEG data
        signal = data[0]  # First channel of data

        # Calculate spectrogram
        frequencies, times, Sxx = spectrogram(signal, fs=fs, nperseg=256, noverlap=128)
        
        # Find indices for beta frequency range (13-30 Hz)
        beta_mask = (frequencies >= 13) & (frequencies <= 30)
        
        # Calculate the average magnitude of beta waves
        beta_magnitude = np.mean(Sxx[beta_mask])

        # Compare beta magnitude to threshold
        if beta_magnitude > threshold:
            print("Beta wave magnitude is high. Please lower your intensity.")

        # Update plot
        ax.clear()
        ax.pcolormesh(times, frequencies[beta_mask], 10 * np.log10(Sxx[beta_mask]), shading='gouraud')
        ax.set_title('Beta Waves Spectrogram (13-30 Hz)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        plt.colorbar(ax.pcolormesh(times, frequencies[beta_mask], 10 * np.log10(Sxx[beta_mask]), shading='gouraud'), ax=ax, label='Power/Frequency (dB/Hz)')
        plt.pause(1)  # Pause for a second to simulate real-time update

        # Sleep for a second to simulate real-time processing
        time.sleep(1)

# Example usage:
# data_stream = YourDataStreamClass()  # This should be a class that provides real-time data
# data_transform_realtime(data_stream, threshold=0.5)