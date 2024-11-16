# import dataTransform
import MAGA
import numpy as np

import matplotlib.pyplot as plt
from matrix_test import random_matrix
from ogData_streaming import data_prepare, data_stream, data_cleanup, stream_length

def plot_frequency_bands(filtered_data):
    """
    Plot the frequency bands using matplotlib.
    
    Args:
        filtered_data: dict of filtered data in different frequency bands
    """
    bands = list(filtered_data.keys())
    values = [np.mean(v) if isinstance(v, (list, np.ndarray)) else v for v in filtered_data.values()]

    plt.figure(figsize=(10, 6))
    plt.bar(bands, values, color=['b', 'g', 'r', 'c', 'm'])
    plt.xlabel('Frequency Bands')
    plt.ylabel('Average Frequency')
    plt.title('Average Frequency in Different EEG Bands')
    plt.show()

def main():
    timeElapsed = 0
    totalTime = 120 #length of time to collect data for in seconds

    board = data_prepare()
    while timeElapsed < totalTime:
        someData = data_stream(board, stream_length)
        filtered_data = MAGA.data_transform(someData)

        for key in filtered_data:
            print(key, ": ", filtered_data[key])

        plot_frequency_bands(filtered_data)

        timeElapsed += stream_length
    data_cleanup()

if __name__ == "__main__":
    main()