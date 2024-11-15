import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import numpy as np

class DataStream:
    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate
        self.params = BrainFlowInputParams()
        self.board = BoardShim(BoardIds.MUSE_2_BOARD, self.params)
        self.board.prepare_session()
        self.board.start_stream()

    def get_next_chunk(self, chunk_size):
        # Wait for enough data to be collected
        time.sleep(chunk_size / self.sampling_rate)
        # Get the latest chunk of data
        data = self.board.get_board_data()
        return data

    def stop(self):
        self.board.stop_stream()
        self.board.release_session()

# Example usage:
# data_stream = DataStream(sampling_rate=256)  # Initialize with the correct sampling rate
# while True:
#     chunk = data_stream.get_next_chunk(chunk_size=256)  # Get 1 second of data
#     # Process the chunk