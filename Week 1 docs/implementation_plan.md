# Week 1: The "Eye" - Implementation Plan

## Goal
Create a computer vision script that reads a video stream (webcam) and detects movement using background subtraction and contour drawing.

## User Review Required
- None at this stage.

## Proposed Changes

### Project Root
#### [NEW] [week1_motion_detection.py](file:///e:/SEM%207/Antigravity%20Project/P01/week1_motion_detection.py)
- Import `cv2` and `numpy`.
- Initialize `cv2.VideoCapture(0)`.
- Initialize `cv2.createBackgroundSubtractorMOG2()`.
- Loop through frames:
    - Apply background subtraction to get mask.
    - Find contours on the mask.
    - Draw green rectangles around significant contours (area filtering to avoid noise).
    - Display the result in a window.
    - Add 'q' key break condition.
    - Cleanup resources.

## Verification Plan
### Automated Tests
- None for this visual interactive script.
### Manual Verification
- Run the script: `python week1_motion_detection.py`
- Verify webcam turns on.
- Verify moving objects (e.g., hand) have green boxes drawn around them.
- Verify static background does not have boxes.
- Verify 'q' quits the application.
