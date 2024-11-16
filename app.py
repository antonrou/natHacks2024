from flask import Flask, render_template, jsonify, request
from ogData_streaming import data_prepare, data_stream, data_cleanup, stream_length
from MAGA import data_transform
import threading #provide support for running multiple threads for concurrent execution
import numpy as np
import matplotlib.pyplot as plt
import io #used for in-memory file handling
import base64 #encodes binary data into a base64 string, useful for embedding images in responses

app = Flask(__name__) #initialize the Flask application

# Global variable to hold the board session
board = None #initializes board as None, indicating that no connection has been established yet

@app.route('/') #defines the route for the home page
def home(): #defines the function that will be executed when the home page is accessed
    return render_template('index.html') #renders the index.html template and returns it as the response

@app.route('/connect_muse', methods=['POST']) #defines the route for connecting to the Muse 2 board
def connect_muse(): #defines the function that will be executed when the connect_muse route is accessed
    global board #declares that the board variable is a global variable
    try:
        board = data_prepare() #establishes a connection to the Muse 2 board
        return jsonify({"status": "Muse 2 connected"}) #returns a JSON response with a status message
    except Exception as e: #catches any exceptions that occur during the connection process
        return jsonify({"error": str(e)}), 500 #returns a JSON response with an error message and a 500 status code if an exception occurs

@app.route('/start_session', methods=['POST']) #defines the route for starting a Pomodoro session
def start_session(): #defines the function that will be executed when the start_session route is accessed
    # Logic to start a Pomodoro session
    return jsonify({"status": "Session started"}) #returns a JSON response with a status message

@app.route('/end_session', methods=['POST']) #defines the route for ending a Pomodoro session
def end_session(): #defines the function that will be executed when the end_session route is accessed
    # Logic to end a Pomodoro session
    return jsonify({"status": "Session ended"}) #returns a JSON response with a status message

@app.route('/brainwave_data', methods=['POST']) #defines the route for receiving brainwave data
def brainwave_data(): #defines the function that will be executed when the brainwave_data route is accessed
    global board #declares that the board variable is a global variable
    if not board: #checks if the board is not connected
        return jsonify({"error": "Muse 2 not connected"}), 400 #returns a JSON response with an error message and a 400 status code if the board is not connected

    try:
        # Collect data from the Muse 2
        data = data_stream(board, stream_length) #collects data from the Muse 2 board
        # Transform the data into frequency bands
        filtered_data = data_transform(data) #transforms the data into frequency bands
        # Plot the frequency bands and return the image
        img = plot_frequency_bands(filtered_data) #plots the frequency bands and returns the image as a base64 string
        return jsonify({"focus": True, "image": img}) #returns a JSON response with a focus status and the image
    except Exception as e: #catches any exceptions that occur during the data collection and transformation process
        return jsonify({"error": str(e)}), 500 #returns a JSON response with an error message and a 500 status code if an exception occurs

def plot_frequency_bands(filtered_data): #defines the function that will be executed when the plot_frequency_bands route is accessed
    """
    Plot the frequency bands using matplotlib and return the image as a base64 string.
    
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

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the image to base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def cleanup_board():
    global board
    if board:
        data_cleanup(board)
        board = None

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    finally:
        cleanup_board()