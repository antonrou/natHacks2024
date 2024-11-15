import brainflow #library for interfacing with Muse 2 board
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds #BoardShim is the main interface to interact with Muse 2 board, BrainFlowInputParams is for input parameters, BoardIds enumerates the different boards
import time #used to add a delay during data collection

params = BrainFlowInputParams() #constructor call that creates a new instance of the BrainFlowInputParams class. Used to specify the input paraemeters required to configure the connection to a specific board
board = BoardShim(BoardIds.MUSE_2_BOARD, params)

def reconnect(board, params):
    #The goal is to reconnect the device after it's disconnected rather than
    # letting it failed#
    print("Reconnecting...")
    board.stop_stream()
    board.release_session()
    time.sleep(1)

    new_board = BoardShim(BoardIds.MUSE_2_BOARD, params)
    new_board.prepare_session()
    new_board.start_stream()
    print("Reconnected Successfully")
    return new_board

try:
    board.prepare_session()
    board.start_stream()

    n = 10
    start_time = time.time() #Track start time#
    #time.time() represents the current timeline#

    while time.time() - start_time < n:
        try:
            if not board.is_prepared():
                board = reconnect(board, params)
            time.sleep(1)
        except Exception as e:
            print(f"Error occurred: {e}")
            board = reconnect(board, params)

    data = board.get_board_data()#data is a numpy 2D array of size num_channels x num_samples.
    print(data.shape) #prints (num_channels, num_samples). Each channel is a different sensor on the Muse 2, the num_samples is the number of samples collected over n seconds
    for i in range(data.shape[0]):  # data.shape[0] gives the number of channels (columns)
        print(f"Column {i+1}: {data[i]}")

finally:
    # Ensure the session is stopped and released even in case of errors
    board.prepare_session()
    board.start_stream()
