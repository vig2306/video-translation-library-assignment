from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

# Simulated delay configuration
PENDING_DELAY = random.randint(80, 120)  # Total seconds until "completed"
start_time = time.time()

@app.route('/status', methods=['GET'])
def get_status():
    elapsed_time = time.time() - start_time
    progress = min(elapsed_time / PENDING_DELAY * 100, 100)  # Calculate progress percentage

    # Simulating status based on time
    if elapsed_time < PENDING_DELAY:
        return jsonify({
            "result": "pending",
            "progress": round(progress, 2),  # Round to 2 decimal places
            "total_delay": PENDING_DELAY,
            "elapsed_time": round(elapsed_time, 2)
        }), 200
    elif random.random() < 0.1:  # Simulate a small chance of error
        return jsonify({"result": "error"}), 200
    else:
        return jsonify({"result": "completed", "progress": 100}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
