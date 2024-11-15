import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import time

def data_transform_realtime(data_stream, n_seconds=10, threshold=0.5):
    fs = data_stream.sampling_rate  # Assume data_stream has a sampling_rate attribute
    chunk_size = fs  # Process 1 second of data at a time

    plt.ion()  # Turn on interactive mode for real-time plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    while True:
        # Get the latest chunk of data
        data = data_stream.get_next_chunk(chunk_size)
        
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