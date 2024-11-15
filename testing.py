import dataTransform
import ogData_streaming

data_stream = ogData_streaming()

dataTransform.data_transform_realtime(data_stream, n_seconds=10, threshold=0.5)