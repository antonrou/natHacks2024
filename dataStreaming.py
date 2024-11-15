import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time

params = BrainFlowInputParams()
board = BoardShim(BoardIds.MUSE_2_BOARD, params)
board.prepare_session()
board.start_stream()

def reconnect(board, params):
    print("Reconnecting...")
    board.stop_stream()
    board.release_session()
    time.sleep(1)
    new_board = BoardShim(BoardIds.MUSE_2_BOARD, params)
    new_board.prepare_session()
    new_board.start_stream()
    print("Reconnected Successfully")
    return new_board

n = 10
start_time = time.time()

try:
    while time.time() - start_time < n:
        try:
            if not board.is_prepared():
                board = reconnect(board, params)
            time.sleep(1)
        except Exception as e:
            print(f"Error occurred: {e}")
            board = reconnect(board, params)

    data = board.get_board_data()
    print(data.shape)

finally:
    board.stop_stream()
    board.release_session()