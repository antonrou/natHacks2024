import brainflow #library for interfacing with Muse 2 board
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds #BoardShim is the main interface to interact with Muse 2 board, BrainFlowInputParams is for input parameters, BoardIds enumerates the different boards
import time #used to add a delay during data collection

def data_stream():
    params = BrainFlowInputParams() #constructor call that creates a new instance of the BrainFlowInputParams class. Used to specify the input paraemeters required to configure the connection to a specific board
    board = BoardShim(BoardIds.MUSE_2_BOARD, params)
    board.prepare_session()
    board.start_stream()
    n = 10 #length of time to collect data for in seconds
    time.sleep(n) #collect data for n seconds
    data = board.get_board_data() #data is a numpy 2D array of size num_channels x num_samples.
    print(data.shape) #prints (num_channels, num_samples). Each channel is a different sensor on the Muse 2, the num_samples is the number of samples collected over n seconds
    #print(data) #prints the data in a 2D array where first element is num of Columns and second element is num of Rows
    board.stop_stream()
    board.release_session()
    return data