import time
from typing import Dict, Any
import numpy as np
from data_calibration import calibration
from data_streaming import data_stream, data_prepare
from data_transform import transform_data

class FocusMonitor:
    
    def __init__(self, recalibrate: bool = False):
        """
        Initialize the focus monitor with calibration data and board setup.
        
        Args:
            recalibrate (bool): Force a new calibration even if saved data exists
        """
        self.board = data_prepare()
        self.thresholds = self._load_or_calibrate(recalibrate)
        self.distraction_count = 0
        self.session_start_time = None
        self.last_distraction_time = None
        
    def _load_or_calibrate(self, recalibrate: bool) -> Dict[str, Any]:
        """Load saved thresholds or perform new calibration."""
        try:
            if recalibrate:
                raise FileNotFoundError  # Force recalibration
            # TODO: Implement loading from saved file
            raise FileNotFoundError
        except FileNotFoundError:
            return calibration()

    def is_distracted(self, current_data: Dict[str, float]) -> bool:
        """
        Check if current brain wave data indicates distraction.
        
        Args:
            current_data: Dictionary of brain wave values
        Returns:
            bool: True if distracted, False if focused
        """
        for wave_type, value in current_data.items():
            if wave_type in self.thresholds:
                if not (self.thresholds[wave_type]['lower'] <= 
                       value <= 
                       self.thresholds[wave_type]['upper']):
                    return True
        return False

    def handle_distraction(self) -> None:
        """Handle detection of distraction event."""
        current_time = time.time()
        
        # Update distraction metrics
        self.distraction_count += 1
        self.last_distraction_time = current_time
        
        # TODO: Implement notification system (could be sound, popup, etc.)
        print("Distraction detected! Please refocus on your task.")

    def get_session_stats(self) -> Dict[str, Any]:
        """Calculate and return session statistics."""
        if not self.session_start_time:
            return {}
            
        current_time = time.time()
        session_duration = current_time - self.session_start_time
        
        return {
            'duration_minutes': session_duration / 60,
            'distraction_count': self.distraction_count,
            'distractions_per_hour': (self.distraction_count * 3600) / session_duration
        }

    def start_monitoring(self, stream_length: int = 256) -> None:
        """
        Start the focus monitoring session.
        
        Args:
            stream_length: Number of data points to collect in each stream
        """
        try:
            self.session_start_time = time.time()
            self.distraction_count = 0
            
            print("Starting focus monitoring session...")
            print("Press Ctrl+C to end the session.")
            
            while True:
                # Get and process EEG data
                raw_data = data_stream(self.board, stream_length)
                transformed_data = transform_data(raw_data)
                
                # Check for distraction
                if self.is_distracted(transformed_data):
                    self.handle_distraction()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            # Handle clean session ending
            print("\nEnding session...")
            stats = self.get_session_stats()
            print("\nSession Statistics:")
            print(f"Duration: {stats['duration_minutes']:.1f} minutes")
            print(f"Total distractions: {stats['distraction_count']}")
            print(f"Distractions per hour: {stats['distractions_per_hour']:.1f}")
        
        finally:
            # Clean up board connection
            if self.board:
                self.board.stop_stream()
                self.board.release_session()

def main():
    """Main entry point for the focus monitor."""
    monitor = FocusMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
