# Week 1: The "Eye" - Implementation Plan

## Goal
Create a computer vision script that reads a video stream (webcam) and detects movement using background subtraction and contour drawing.

## User Review Required
- None at this stage.

## Proposed Changes

### [verify_week1.py](file:///e:/SEM%207/Antigravity%20Project/P01/week1_motion_detection.py)
*(Already implemented)*

# Week 2: The "Brain" - Implementation Plan

## Goal
Upgrade from simple motion detection to smart object detection using YOLOv8 to identify humans.

## User Review Required
- None.

## Proposed Changes

### Project Root
#### [NEW] [week2_object_detection.py](file:///e:/SEM%207/Antigravity%20Project/P01/week2_object_detection.py)
- Import `cv2` and `ultralytics`.
- Initialize `YOLO('yolov8n.pt')` model.
- Initialize `cv2.VideoCapture(0)`.
- Loop through frames:
    - Run inference: `results = model(frame)`.
    - Iterate results.
    - Check if `class == 'person'` (class ID 0) and `conf > 0.5`.
    - Draw red bounding boxes and labels using `cv2.rectangle` and `cv2.putText`.
    - Display result.
    - Add 'q' key break.

## Verification Plan
### Manual Verification
- Run `python week2_object_detection.py`.
- Verify it downloads the model weights on first run.
- Verify it specifically detects people with a red box.
- Verify it ignores other moving objects (like a waving chair or other non-human objects if possible to test).

### [verify_week2.py](file:///e:/SEM%207/Antigravity%20Project/P01/week2_object_detection.py)
*(Already implemented)*

# Week 3: The "System" - Implementation Plan

## Goal
Turn the object detection component into a full security product with logging, snapshots, cooldowns, and performance metrics.

## User Review Required
- None.

## Proposed Changes

### Project Root
#### [NEW] [main.py](file:///e:/SEM%207/Antigravity%20Project/P01/main.py)
- Import `cv2`, `time`, `os`, `ultralytics`.
- Ensure directory `Intruder_Logs` exists.
- Initialize `YOLO` model and `VideoCapture`.
- Initialize `last_snapshot_time = 0` (for cooldown).
- Loop frames:
    - Calculate FPS.
    - Run inference.
    - Detect 'person' with confidence > 0.5.
    - Drawing: Red box around person.
    - Overlay: "Status: INTRUDER DETECTED" (Red) vs "Status: Monitoring" (Green).
    - Snapshot Logic:
        - If person detected AND `(current_time - last_snapshot_time) > 5`:
        - Save frame to `Intruder_Logs/intruder_{timestamp}.jpg`.
        - Update `last_snapshot_time`.
    - Display FPS on frame.
    - 'q' to quit.

## Verification Plan
### Manual Verification
- Run `python main.py`.
- Walk in front of camera.
- Verify "INTRUDER DETECTED" text appears.
- Verify snapshot is saved to `Intruder_Logs`.
- Wait < 5 seconds and move again -> Verify NO new snapshot is saved (cooldown).
- Wait > 5 seconds and move again -> Verify NEW snapshot is saved.
- Check stored images for correct naming convention.
