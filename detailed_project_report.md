# Aerial Watch: Drone-Based Intruder Detection System
## Detailed Technical Report

### 1. Executive Summary

**Aerial Watch** is a software-based security solution designed to simulate a drone-based surveillance system. The primary objective is to detect potential intruders (humans) from a video feed in real-time using advanced computer vision and deep learning technologies.

This project evolved over three distinct phases (weeks), starting from basic motion detection and advancing to sophisticated object recognition with a web-based user interface. The final system is a robust, dual-interface product capable of processing live camera feeds or pre-recorded video files, identifying threats, and logging evidence automatically.

### 2. Project Objectives

1.  **Develop a Vision System**: Create a pipeline to process video frames efficiently.
2.  **Implement Smart Detection**: Move beyond simple motion detection to specific object classification (Person vs. Others).
3.  **Build a Security Product**: Turn the detection logic into a usable system with logs, alerts, and user controls.
4.  **Create Modern Interfaces**: Provide both a developer-friendly CLI and a user-friendly Web Dashboard.

### 3. System Architecture

The system utilizes a modular architecture designed for flexibility and performance.

#### 3.1 Technology Stack
*   **Core Language**: Python 3.11
*   **Computer Vision**: OpenCV (Open Source Computer Vision Library)
*   **Deep Learning Model**: YOLOv8 Nano (Ultralytics) - Chosen for its high speed and accuracy suitable for edge devices.
*   **Web Framework**: Flask (Python) - Serves the backend API and video stream.
*   **Frontend**: HTML5, CSS3, JavaScript - Provides the interactive dashboard.

#### 3.2 Detection Pipeline (The "Brain")
1.  **Input Acquisition**: Captures video frame from Webcam (Index 0) or Video File using OpenCV.
2.  **Preprocessing**: Resizes frames (if necessary) for consistent processing speed.
3.  **Inference**:
    *   The frame is passed to the YOLOv8 Nano model.
    *   The model returns a list of detected objects with class IDs and confidence scores.
4.  **Filtering Logic**:
    *   Iterates through detections.
    *   **Condition 1**: Class must be `'person'`.
    *   **Condition 2**: Confidence score must be `> 0.5` (50%).
5.  **Evidence Logging**:
    *   If a threat is detected, the system checks the **Cooldown Timer** (5 seconds).
    *   If the timer allows, the current frame is saved to `Intruder_Logs/` with a timestamp.

### 4. Implementation Phase Details

#### Phase 1: The "Eye" - Motion Detection (Week 1)
*   **Goal**: Detect any movement.
*   **Method**: Used Background Subtraction (MOG2). It learned the static background and highlighted changing pixels.
*   **Limitation**: Detected *everything* moving (trees, birds, shadows), causing false alarms.

#### Phase 2: The "Brain" - Object Detection (Week 2)
*   **Goal**: Smart Detection.
*   **Method**: Integrated YOLOv8.
*   **Result**: The system could now distinguish a human from a moving tree branch. We implemented the bounding box visualization (Red Box) and confidence labeling.

#### Phase 3: The "System" & Frontend (Week 3+)
*   **Goal**: Full Productization.
*   **System Logic**: Added automatic snapshot logging, cooldown timers, FPS counters, and on-screen status alerts.
*   **Web Interface**: Developed a Flask application to stream the processed video to a browser. Implemented a gallery to view captured snapshots in real-time.

### 5. Detailed Features

#### 5.1 Dual Mode Interface
*   **CLI Mode (`main.py`)**: Runs directly in the terminal/console window. Best for debugging and low-resource environments.
*   **Web Mode (`app.py`)**: Runs a local web server (`localhost:5000`). Features a modern UI with start/stop buttons, source selection dropdowns, and a live evidence gallery.

#### 5.2 Intelligent Logging
To prevent disk flooding, the system uses a smart logic gate:
```python
if intruder_detected and (current_time - last_snapshot_time > 5):
    save_snapshot()
    update_timer()
```
This ensures that a continuous intruder presence doesn't generate thousands of identical images, but rather one high-quality snapshot every 5 seconds.

#### 5.3 Video Streaming (MJPEG)
The web interface uses **Motion JPEG** streaming. This technique sends a continuous stream of JPEG images to the browser. It allows for low-latency video monitoring that works natively in all modern web browsers without plugins.

### 6. Testing & Results

#### 6.1 Performance
*   **FPS (Frames Per Second)**: consistently achieves 30+ FPS on standard laptop hardware (CPU only) usage due to the efficiency of the Nano model.
*   **Latency**: The web interface shows minimal latency (<200ms) on a local network.

#### 6.2 Accuracy
*   **True Positives**: Successfully detected human subjects at various distances and angles.
*   **False Positives**: Drastically reduced compared to the Week 1 motion detection method. The confidence threshold of 0.5 effectively filters out weak matches.

### 7. Future Enhancements

1.  **Hardware Integration**: Deploy the code onto a Raspberry Pi or NVIDIA Jetson attached to an actual drone.
2.  **Notification System**: Integrate email or SMS APIs (e.g., Twilio) to send alerts to a phone when an intruder is detected.
3.  **Cloud Storage**: Upload snapshots to a cloud bucket (AWS S3/Google Cloud Storage) for off-site backup.
4.  **Face Recognition**: Add a "Allowed Persons" list to ignore known individuals.

### 8. Conclusion

Aerial Watch successfully demonstrates the power of modern AI in security applications. By combining efficient deep learning with standard web technologies, we created a professional-grade prototype that is both effective and easy to use. The transition from simple motion detection to AI-based object recognition highlights the significant leap in capability provided by neural networks.
