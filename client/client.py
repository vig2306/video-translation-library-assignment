import math
import requests
import time
import random

class VideoTranslationClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_status(self):
        try:
            response = requests.get(f"{self.base_url}/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def poll_status(self, initial_interval=5, max_interval=10, initial_frequent_interval=5, min_interval=0.5, k=0.1, max_retries=50):
        """
        Polls the server with dynamic interval adjustment based on progress.
        Args:
            initial_interval (int): Initial polling interval (seconds) for progress < 60%.
            max_interval (int): Maximum polling interval (seconds) for progress < 60%.
            initial_frequent_interval (int): Starting interval for frequent polling.
            min_interval (float): Minimum interval for frequent polling.
            k (float): Decay factor for exponential decay.
            max_retries (int): Maximum number of polling attempts.
        """
        retries = 0
        interval = initial_interval
        start_time = time.time()  # Track when polling starts

        while retries < max_retries:
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            status = self.get_status()

            # Get progress and result from the server response
            progress = status.get("progress", 0)
            result = status.get("result")
            print(f"Attempt {retries + 1}: Status: {result}, Progress: {progress}%, Elapsed Time: {round(elapsed_time, 2)} seconds")

            # Exit polling loop if status is "completed" or "error"
            if result in ("completed", "error"):
                return status

            # Adjust polling interval based on progress
            if progress >= 60:
                # Smooth decay as progress approaches 100%
                interval = max(
                    min_interval,
                    initial_frequent_interval * math.exp(-k * (100 - progress))
                )
            else:
                # Exponential backoff for progress < 70%
                interval = min(interval * 2, max_interval)

            # Add jitter for randomness
            jitter = random.uniform(-0.1 * interval, 0.1 * interval)
            next_interval = interval + jitter

            # Sleep before the next attempt
            time.sleep(next_interval)

            retries += 1

        # If max retries are reached, return the last status
        return {"error": "Polling timed out", "last_status": status}
