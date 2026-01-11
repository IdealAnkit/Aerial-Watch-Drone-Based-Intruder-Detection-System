# Learning Guide: Week 1 Motion Detection

This document provides a line-by-line breakdown of the `week1_motion_detection.py` script. It explains not just *what* the code does, but *why* it is written that way, introducing key Computer Vision concepts.

## 1. Imports

```python
import cv2
import numpy as np
```

-   `import cv2`: Imports the OpenCV library, which is the core tool we use for computer vision tasks (reading video, processing images, detecting motion).
-   `import numpy as np`: Imports NumPy, a powerful library for numerical operations. Images in OpenCV are essentially stored as huge matrices (grids) of numbers, so NumPy is used heavily for manipulating these matrices.

## 2. Main Function Setup

```python
def main():
    """
    Main function to run the motion detection.
    """
```

-   Standard Python practice to wrap the main logic in a function. This keeps the code organized.

## 3. Video Capture Initialization

```python
    # Initialize video capture from default camera (index 0)
    # If using a drone stream, replace 0 with the RTSP/UDP URL
    cap = cv2.VideoCapture(0)
```

-   `cv2.VideoCapture(0)`: This line connects to your video source.
    -   `0` refers to the *first* webcam connected to your computer (usually the built-in laptop camera).
    -   If you were using a drone, you would replace `0` with a stream URL like `'udp://192.168.10.1:11111'`.

## 4. The Motion Detector (Background Subtraction)

```python
    # Initialize background subtractor
    # MOG2 is a Gaussian Mixture-based Background/Foreground Segmentation Algorithm
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
```

-   **Concept**: To detect motion, we need to know what is "background" (static) and what is "foreground" (moving).
-   `cv2.createBackgroundSubtractorMOG2(...)`: Creates a special object that "learns" the background over time.
    -   `history=500`: The model remembers the last 500 frames to decide what the static background looks like.
    -   `varThreshold=50`: Sensitivity. Lower values detect smaller changes (more sensitive), higher values ignore small changes.
    -   `detectShadows=True`: The algorithm attempts to classify shadows (usually gray) separately from real moving objects (white). We will filter these out later.

## 5. Main Loop

```python
    while True:
        ret, frame = cap.read()
```

-   `while True`: An infinite loop that runs until we manually stop it. This is standard for processing live video streams.
-   `cap.read()`: Grabs the next frame (image) from the camera.
    -   `ret`: A boolean (True/False). `True` if the frame was read successfully.
    -   `frame`: The actual image data (a NumPy array).

## 6. Processing the Frame

```python
        # Apply background subtraction to get the foreground mask
        fg_mask = back_sub.apply(frame)
```

-   `back_sub.apply(frame)`: This is the magic step. It compares the current `frame` against the "learned" background.
-   **Result (`fg_mask`)**: This is a black-and-white image (mask).
    -   **Black pixels (0)**: Things that haven't changed (background).
    -   **White pixels (255)**: Things that moved (foreground).
    -   **Gray pixels (127)**: Shadows (if `detectShadows=True`).

## 7. Cleaning up the Mask

```python
        # Clean up the mask: remove shadows (which are usually gray in MOG2)
        # Thresholding ensures we only get the moving objects (white)
        _, fg_mask_clean = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
```

-   **Why?** The MOG2 algorithm might detect shadows, which we don't want to count as "intruders".
-   `cv2.threshold(...)`: A filter that says "only keep pixels that are super bright".
    -   We set the threshold to `250`. Since white is `255` and shadows are usually around `127`, this purely keeps the moving objects and turns everything else black.

```python
        # Optional: Morphological operations to remove noise (small white dots)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask_clean = cv2.morphologyEx(fg_mask_clean, cv2.MORPH_OPEN, kernel)
```

-   **Concept**: Digital cameras have "noise" (random specks). We want to erase those.
-   `cv2.morphologyEx(..., cv2.MORPH_OPEN, ...)`: This is an "Opening" operation. It's like an eraser that only rubs out small isolated dots but leaves big blobs alone.

## 8. Finding Objects (Contours)

```python
        # Find contours on the mask
        contours, _ = cv2.findContours(fg_mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

-   **Concept**: Now that we have a clean black-and-white image where white blobs are moving people/objects, we need to find the boundaries of those blobs.
-   `cv2.findContours(...)`: Returns a list of all separate white blobs found in the image.

## 9. Drawing Boxes

```python
        for contour in contours:
            # Filter out small movements/noise based on area
            if cv2.contourArea(contour) < 500:
                continue

            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw green rectangle around the object
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

-   `for contour in contours`: Loop through every blob found.
-   `cv2.contourArea(contour) < 500`: **Critical step**. If a blob is too small (less than 500 pixels area), ignore it. This prevents the system from detecting a bug flying by or slight wind movement.
-   `cv2.boundingRect(contour)`: Calculates the simple upright rectangle `(x, y, width, height)` that fully contains the blob.
-   `cv2.rectangle(...)`: Draws that box onto the original color `frame` so the user can see it. `(0, 255, 0)` is Green.

## 10. Display and Exit

```python
        # Display the resulting frame
        cv2.imshow('Aerial Watch - Motion Detection', frame)
```

-   `cv2.imshow(...)`: Pops up a window on your screen showing the video with the boxes drawn on it.

```python
        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

-   `cv2.waitKey(1)`: Waits 1 millisecond for a key press.
-   `& 0xFF == ord('q')`: Checks if that key was 'q'. If so, it breaks the `while` loop.

## 11. Cleanup

```python
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
```

-   `cap.release()`: Creates a "polite" exit. It tells Windows/MacOS "I'm done with the camera, other apps can use it now."
-   `cv2.destroyAllWindows()`: Closes the popup window.
