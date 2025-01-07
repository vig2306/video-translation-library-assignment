import sys
import os
import threading
import subprocess
import time

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client.client import VideoTranslationClient

def run_server():
    # Start the Flask server as a subprocess
    server_process = subprocess.Popen(["python", "../server/server.py"])
    return server_process

def test_polling_with_decay():
    # Start the server
    server_process = run_server()
    time.sleep(2)  # Wait for server to start

    try:
        # Initialize client and poll with decay
        client = VideoTranslationClient("http://127.0.0.1:5000")
        final_status = client.poll_status(initial_interval=1, max_interval=30, initial_frequent_interval=5, min_interval=0.5, max_retries=50)
        print("Final Status:", final_status)  # Print the final status
        assert final_status["result"] in ("completed", "error")
    finally:
        # Terminate the server after testing
        server_process.terminate()
        server_process.wait()
        print("Server terminated.")

# Main execution block
if __name__ == "__main__":
    test_polling_with_decay()
