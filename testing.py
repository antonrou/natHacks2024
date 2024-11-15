import dataTransform
from dataStreaming import DataStream

# Initialize the data stream with the correct sampling rate
sampling_rate = 256  # Example sampling rate, adjust as needed
data_stream = DataStream(sampling_rate=sampling_rate)

# Call the data_transform_realtime function with the data stream
dataTransform.data_transform_realtime(data_stream, threshold=0.5)