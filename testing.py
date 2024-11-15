import dataTransform
from dataStreaming import DataStream

data_stream = DataStream()
dataTransform.data_transform_realtime(data_stream, n_seconds=10, threshold=0.5)