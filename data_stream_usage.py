from streaming import DataStream  # Replace 'your_module' with the actual module name

def main():
    # Initialize the DataStream with the correct sampling rate
    data_stream = DataStream(sampling_rate=256)

    try:
        while True:
            # Get a chunk of data (e.g., 1 second of data if chunk_size is 256)
            chunk = data_stream.get_next_chunk(chunk_size=256)
            
            # Process the chunk
            # For example, you might print the shape of the data
            print("Data chunk shape:", chunk.shape)
            
            # Add your data processing logic here
            # e.g., filtering, feature extraction, etc.

    except KeyboardInterrupt:
        # Stop the data stream when you interrupt the program (e.g., Ctrl+C)
        print("Stopping data stream...")

    finally:
        # Ensure the stream is stopped and the session is released
        data_stream.stop()
        print("Data stream stopped.")

if __name__ == "__main__":
    main()