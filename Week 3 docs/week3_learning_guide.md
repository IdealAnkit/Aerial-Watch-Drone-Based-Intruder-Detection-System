# Learning Guide: Week 3 The "System" (main.py)

This document explains the final `main.py` script which turns our object detector into a full security product.

## 1. Imports

```python
import cv2
import time
import os
import datetime
from ultralytics import YOLO
```

-   `import time`: Used for the **cooldown timer** (checking how many seconds passed).
-   `import os`: Used to check if the `Intruder_Logs` folder exists and create it if not.
-   `import datetime`: Used to create timestamps for filenames (e.g., `2025-12-29_10-30.jpg`).

## 2. Environment Setup

```python
    # Ensure the logs directory exists
    log_dir = "Intruder_Logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")
```

-   **Why?** If we try to save an image to a folder that doesn't exist, Python will crash.
-   `os.makedirs(log_dir)`: Automatically creates the folder for us.

## 3. Source Selection (Interactive Input)

```python
    # 2. User Input: Select Source
    print("\n=== Aerial Watch - Source Selection ===")
    print("1. Live Camera")
    print("2. Video File (from Demo Video folder)")
    choice = input("Enter your choice (1 or 2): ").strip()
```

-   **Purpose**: This makes the system flexible. You can test with pre-recorded footage OR use a live camera.
-   `input(...)`: Pauses the program and waits for the user to type something.
-   `.strip()`: Removes extra spaces (in case the user types "1 " instead of "1").

### Camera Selection (Option 1)

```python
    if choice == '1':
        print("Initializing camera...")
        cap = cv2.VideoCapture(0)
        source_name = "Camera"
```

-   Simple: Just opens the default camera at index `0`.

### Video File Selection (Option 2)

```python
    elif choice == '2':
        demo_folder = "Demo Video"
        if os.path.exists(demo_folder):
            video_files = [f for f in os.listdir(demo_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
```

-   **`os.listdir(demo_folder)`**: Gets all files in the Demo Video folder.
-   **List Comprehension**: We filter only video files by checking if they end with `.mp4`, `.avi`, `.mov`, or `.mkv`.

```python
            if video_files:
                print(f"\nAvailable videos in '{demo_folder}':")
                for i, vf in enumerate(video_files, 1):
                    print(f"  {i}. {vf}")
```

-   **`enumerate(video_files, 1)`**: Creates a numbered list starting from 1 (user-friendly).
-   Displays all available videos so the user can pick one.

```python
                video_choice = input(f"Select video (1-{len(video_files)}): ").strip()
                try:
                    video_index = int(video_choice) - 1
                    if 0 <= video_index < len(video_files):
                        video_path = os.path.join(demo_folder, video_files[video_index])
                        cap = cv2.VideoCapture(video_path)
```

-   **Error Handling**: We use `try-except` to catch if the user types something that's not a number.
-   **Index Conversion**: User sees "1, 2, 3...", but Python lists use "0, 1, 2...", so we subtract 1.
-   **`os.path.join(...)`**: Safely combines folder name and filename (works on Windows/Mac/Linux).

## 4. System Variables (The Logic)

```python
    last_snapshot_time = 0
    cooldown_seconds = 5
```

-   **`last_snapshot_time`**: Stores the exact time (in seconds) when we last took a photo. Initially 0.
-   **`cooldown_seconds = 5`**: The rule—we must wait 5 seconds between photos.

## 5. FPS Calculation (Performance)

```python
        # Calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = new_frame_time
```

-   **Formula**: FPS = 1 / (Time taken to process this frame).
-   If it takes 0.1 seconds to process a frame, then 1 / 0.1 = 10 FPS.

## 6. Security Logic (The "If" Statement)

```python
                # Security Logic: Only look for 'person' with high confidence
                if name == 'person' and conf > 0.5:
                    intruder_detected = True
```

-   We set a flag `intruder_detected = True` if we see a person. We use this flag later to decide whether to trigger the alarm.

## 7. The Alarm System (Snapshots)

```python
        if intruder_detected:
            # Automatic Snapshot with Cooldown
            current_time = time.time()
            if current_time - last_snapshot_time > cooldown_seconds:
```

-   **The Check**: "Is there an intruder?" AND "Has it been more than 5 seconds since the last photo?"

```python
                # Generate filename: intruder_YYYY-MM-DD_HH-MM-SS.jpg
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{log_dir}/intruder_{timestamp}.jpg"
                
                # Save the frame
                cv2.imwrite(filename, frame)
```

-   `cv2.imwrite(...)`: Saves the current video frame as an image file on your hard drive.
-   **Timestamping**: Crucial for evidence. We format the time so files sort chronologically.

## 8. Status Overlay (UI)

```python
            # Visual Alert on Screen
            cv2.putText(frame, "STATUS: INTRUDER DETECTED", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
```

-   **Red Text**: `(0, 0, 255)` tells the human operator something is wrong.
-   **Green Text** (in the `else` block): Tells the operator the system is working normally.

## Summary

This script adds four layers of "polish" to the Week 2 detection code:
1.  **Interactive Source Selection**: Choose between live camera or pre-recorded video files.
2.  **File System Management**: Creating folders automatically and handling video files.
3.  **Logic Gates**: The Cooldown Timer prevents spamming.
4.  **User Interface**: FPS and Status text make it look like a professional tool.
