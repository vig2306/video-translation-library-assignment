# Translation Client Library

## Overview


The library:
- Reduces unnecessary network requests with **exponential backoff** during early stages.
- Increases polling frequency with **exponential decay** as progress surpasses 60%.
- Uses **jitter** to avoid synchronized requests.

---

## Getting Started

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/video_translation_library.git
cd video_translation_library
```

### Prerequisites

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Approach

### Adaptive Polling Strategy

The polling strategy dynamically adjusts intervals based on the **progress** reported by the server:
1. **Exponential Backoff**:
   - For progress < 60%, the polling interval doubles after each attempt (capped by `max_interval`).
   - This reduces server load during the early stages of video translation.

2. **Exponential Decay**:
   - For progress ≥ 60%, the interval decreases smoothly as progress approaches 100%.
   - Formula:
     \[
     \text{interval} = \max(\text{min\_interval}, \text{initial\_frequent\_interval} \times e^{-k \cdot (100 - \text{progress})})
     \]
     - \( k \): Decay factor to control how quickly the interval reduces.
     - This ensures more frequent polling as the job nears completion.

3. **Jitter**:
   - A random factor is added to intervals to avoid synchronized requests:
     \[
     \text{next\_interval} = \text{interval} + \text{jitter}
     \]

---

## Running the Server

The server simulates a video translation backend. Start it with:

```bash
python server/server.py
```

The server will run on `http://localhost:5000` and provide simulated progress updates. You will see logs like:

```plaintext
 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## Using the Client Library

The client library provides an interface to repeatedly query the server until the job is completed or fails. Here’s an example:

```python
from client.client import VideoTranslationClient

# Initialize the client with the server URL
client = VideoTranslationClient("http://localhost:5000")

# Poll the server for the final status
final_status = client.poll_status()
print(f"Final Status: {final_status}")
```

### Key Features:
1. **Dynamic Polling**:
   - Automatically adjusts intervals based on progress.
2. **Error Handling**:
   - Handles network failures gracefully by returning an error status.
3. **Comprehensive Logging**:
   - Logs progress, status, and polling intervals at each step.

---

## Integration Test

The integration test demonstrates the functionality of the client library by:
1. Spinning up the server as a subprocess.
2. Using the client library to fetch job status.
3. Automatically terminating the server after the test.

### Running the Test

Execute the integration test with:

```bash
pytest tests/
```

You’ll see logs like:

```plaintext
Attempt 1: Status: pending, Progress: 5.0%, Elapsed Time: 0.0 seconds
Attempt 2: Status: pending, Progress: 20.0%, Elapsed Time: 10.12 seconds
Attempt 3: Status: pending, Progress: 45.0%, Elapsed Time: 25.34 seconds
Attempt 4: Status: completed, Progress: 100.0%, Elapsed Time: 45.67 seconds
```

---

## Implementation Details

### `poll_status` Method

#### Early Stages (Progress < 60%)
- **Exponential Backoff**:
  - The interval doubles after each polling attempt.
  - Example: 5s → 10s → 20s (capped by `max_interval`).

#### Later Stages (Progress ≥ 70%)
- **Exponential Decay**:
  - The interval decreases as progress approaches 100%.
  - Formula:
    \[
    \text{interval} = \max(\text{min\_interval}, \text{initial\_frequent\_interval} \times e^{-k \cdot (100 - \text{progress})})
    \]

#### Jitter
- Randomness is added to intervals:
  - \( \text{jitter} = \text{random.uniform}(0, \text{interval} / 2) \)
  - Helps avoid synchronized hits from multiple clients.

---

### Server Behavior

- Simulates video translation with a configurable random delay (1–3 minutes).
- Responds with:
  - `progress`: Job progress (0–100%).
  - `result`: Job status (`pending`, `completed`, or `error`).

---

## Conclusion

The Translation Client Library efficiently interacts with a simulated video translation backend using an adaptive polling strategy. It:
- Reduces server load with exponential backoff during early stages.
- Ensures responsiveness with exponential decay as the job nears completion.
- Handles errors gracefully and logs detailed information for monitoring and debugging.