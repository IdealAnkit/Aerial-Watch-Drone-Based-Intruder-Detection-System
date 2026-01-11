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
