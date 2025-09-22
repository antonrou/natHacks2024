# natHacks2024 – Muse 2 Pomodoro Focus Monitor

This project was created during the natHacks 2024 hackathon. It is a web-based Pomodoro timer that uses a Muse 2 EEG headband to monitor your concentration levels while studying.

## Features

- **Real-time focus monitoring:** Detects when you are distracted or focused using brainwave data from the Muse 2.
- **Pomodoro timer:** Standard 25-minute study sessions with break reminders.
- **Visual feedback:** See your brainwave frequency bands and get alerts if you lose focus.

## How to Run

1. **Install dependencies**
   ```zsh
   pip install -r requirements.txt
   ```

2. **Connect your Muse 2 device**
   Make sure your Muse 2 EEG headband is paired and ready.

3. **Start the Flask web server**
   ```zsh
   python app.py
   ```

4. **Open the web interface**
   Go to [http://localhost:5001](http://localhost:5001) in your browser.

5. **Start monitoring**
   - Click "Connect Muse 2" to connect your device.
   - Click "Start Session" to begin a Pomodoro session.
   - The app will alert you if you lose focus.

## Project Structure

- `app.py` – Main Flask web server
- `data_streaming.py` – Handles Muse 2 data collection
- `data_transform.py` – Processes EEG data into frequency bands
- `data_calibration.py` – Calibrates focus/distraction thresholds
- `focus_monitor.py` – Focus monitoring logic
- `templates/index.html` – Web interface

## Requirements

- Python 3.11+
- Muse 2 EEG headband
- See `requirements.txt` for Python dependencies

---

## About This Project

Developed during the natHacks 2024 neurotech hackathon, this project is a personalized Pomodoro focus timer powered by EEG. The timer analyzes real-time brainwave data to assess concentration levels and dynamically adjusts work and break intervals for optimal productivity.

### Key Features

- Monitors beta wave activity (indicative of focus) using the Muse 2 EEG device and the BrainFlow Python library.
- Implements Fast Fourier Transforms (FFTs) to analyze EEG signals and detect dips in focus levels.
- User-friendly front end to visualize focus levels and provide personalized break recommendations.

### Contributions

- Implemented the EEG data streaming process to capture and store brainwave signals accurately.
- Developed signal analysis algorithms using FFTs to detect focus patterns.
- Collaborated on the design and implementation of the web interface and personalized break logic.

**Authors:**
- Anton Roupassov-Ruiz
- Ali Senol
- Willy Zuo
- Advi Islam
- Arno Xu

Created at natHacks 2024.