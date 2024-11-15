import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time

params = BrainFlowInputParams()
board = BoardShim(BoardIds.MUSE_2_BOARD, params)
board.prepare_session()
board.start_stream()

time.sleep(10)
data = board.get_board_data()
print(data.shape)

board.stop_stream()
board.release_session()