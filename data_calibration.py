# This file is used to callibrate the thresholds for each frequency range to determine if the user is in a focused or distracted state.

from data_streaming import data_stream, data_prepare, stream_length
from data_transform import data_transform
import random

def calibration():

    focused_data = find_focus()
    distracted_data = find_distracted_threshold()

    def create_thresholds(focused_data, distracted_data):
        thresholds = {}
        for wave_type in focused_data:

            # Calculate the difference between focused and distracted states
            difference = abs(focused_data[wave_type] - distracted_data[wave_type])
            
            # Create a range buffer (e.g., 20% of the difference)
            buffer = difference * 0.2
            
            # Store both upper and lower bounds
            thresholds[wave_type] = {
                'lower': min(focused_data[wave_type], distracted_data[wave_type]) + buffer,
                'upper': max(focused_data[wave_type], distracted_data[wave_type]) - buffer
            }

        return thresholds
    
    thresholds = create_thresholds(focused_data, distracted_data)

    return thresholds

def find_focus() -> dict: # returns a dictionary with the aveage magnitude of each category of waves for the focused state

    # Collect data from the user while they are in a focused state
    # Use the data to find the magnitudes of each category of waves for a focused state.

    # display simple math equation to user and ask them to solve it.
    # call data_stream function to collect data from the user
    # use data_transform function to transform the data into magnitudes of each category of waves
    # return a dict with the magnitudes of each category of waves that will act as the base values to compare to in the distracted state

    focused_data = {}
    board = data_prepare()
    
    # Could store running averages of readings
    readings = []
    
    while len(readings) < 10:  # Collect 10 samples while solving math
        # Generate random simple math problem
        num1, num2 = random.randint(1, 20), random.randint(1, 20)
        correct_answer = num1 + num2
        
        # In a webapp, this would be displayed on frontend
        print(f"Solve: {num1} + {num2} = ?")
        
        # Collect EEG data while user is solving

        data = data_stream(board, stream_length) # Hinges on a long enough time period that will allow for a focused state and not a flash of math problems being hit at the user.

        filtered_data = data_transform(data)
        readings.append(filtered_data)
        
        # Optional: verify user is actually focusing by checking answer
        user_answer = input("Your answer: ")
        
    # Average all readings
    focused_data = calculate_average_readings(readings)

    return focused_data

def find_distracted_threshold() -> dict:
    distracted_data = {}
    board = data_prepare()
    
    readings = []
    
    while len(readings) < 10:
        num1, num2 = random.randint(1, 20), random.randint(1, 20)
        correct_answer = num1 + num2
        
        print(f"Try to solve while watching the video: {num1} + {num2} = ?")
        # In a webapp, we'd start the video here
        
        # Collect data WHILE user is thinking/solving
        data = data_stream(board, stream_length)  # This should cover the thinking period
        filtered_data = data_transform(data)
        readings.append(filtered_data)
        
        user_answer = input("Your answer: ")  # This happens after data collection
    
    distracted_data = calculate_average_readings(readings)
    return distracted_data

def calculate_average_readings(readings: list) -> dict: # Takes in a list of dictionaries and returns a dictionary with the average magnitude of each category of waves

    dict = {}

    for reading in readings:
        for key in reading:
            if key not in dict:
                dict[key] = reading[key]
            else:
                dict[key] += reading[key]

    for key in dict:
        dict[key] = dict[key] / len(readings)

    return dict
