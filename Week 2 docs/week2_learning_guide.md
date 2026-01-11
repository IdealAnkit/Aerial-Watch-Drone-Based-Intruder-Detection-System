# Learning Guide: Week 2 Object Detection (The "Brain")

This document explains the `week2_object_detection.py` script, focusing on how we use Deep Learning (YOLOv8) to strictly identify humans.

## 1. Imports

```python
import cv2
from ultralytics import YOLO
```

-   `from ultralytics import YOLO`: This imports the YOLO class from the `ultralytics` library. YOLO (You Only Look Once) is a state-of-the-art object detection model that is fast enough for real-time video.

## 2. Model Initialization

```python
    # Load the YOLOv8 Nano model
    # This will automatically download 'yolov8n.pt' if not present
    print("Loading YOLOv8 model... (this might take a moment)")
    model = YOLO('yolov8n.pt')
```

-   `YOLO('yolov8n.pt')`:
    -   **`yolov8n`**: stands for "Nano". It's the smallest, fastest version of YOLOv8. Perfect for laptops or drones where speed matters more than catching every tiny detail.
    -   **`.pt`**: PyTorch weights file. It contains the "brain" that has already learned what 80 different objects (people, cars, dogs, etc.) look like from the COCO dataset.
    -   **Auto-download**: The first time you run this, it downloads the file from the internet.

## 3. The Inference Loop

```python
        # Run inference on the frame
        # stream=True is recommended for video sources to manage memory better
        results = model(frame, stream=True)
```

-   `model(frame)`: This is where we pass our image (frame) to the brain.
-   `stream=True`: This tells the model "I'm sending you a continuous stream of video, not just one photo". It forces the model to use a generator, which is more memory efficient.

## 4. Processing Results

```python
        # Process results
        for result in results:
            boxes = result.boxes
            for box in boxes:
```

-   `result.boxes`: A list of all objects detected in the current frame.
-   We loop through every detected box to decide if we want to keep it or ignore it.

## 5. Understanding the Box Data

```python
                # Get class ID
                cls_id = int(box.cls[0])
                
                # Get confidence score
                conf = float(box.conf[0])

                # Get class name
                name = model.names[cls_id]
```

-   **`box.cls`**: The ID number of the object type (e.g., `0` is usually "person").
-   **`box.conf`**: How sure the robot is. `0.9` means "90% sure this is a X".
-   **`model.names[cls_id]`**: Converts the number `0` to the word `"person"`.

## 6. The Filter (The "Brain" Logic)

```python
                # Filter Logic: Check if it's a Person and confidence > 0.5
                if name == 'person' and conf > 0.5:
```

-   **The Upgrade**: In Week 1, we just checked for *motion*. A blowing tree branch would trigger it.
-   **The Fix**: Now we specifically ask: "Is this object a **person**?" AND "Are you at least **50% sure**?".
    -   If it's a chair moving? `name` will be 'chair'. Ignored.
    -   If it's a person standing still? It might still be detected if visible! (Unlike motion detection which requires movement).

## 7. Drawing and Labeling

```python
                    # Get bounding box coordinates
                    # xyxy format: x1, y1, x2, y2
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Draw Red Box around the person (BGR: 0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
```

-   **`box.xyxy`**: Gives us the corners of the box: Top-Left (x1, y1) and Bottom-Right (x2, y2).
-   **`map(int, ...)`**: Coordinates must be integers (pixel numbers), but the model returns floats (decimals). We convert them.
-   **Color**: In Week 1 we used Green. Here we use Red `(0, 0, 255)` to signify "Intruder Alert" style.

## Summary: Week 1 vs Week 2

| Feature | Week 1 (Motion) | Week 2 (YOLO) |
| :--- | :--- | :--- |
| **Trigger** | Any pixel change | Specific object shape |
| **False Alarms** | High (wind, lights) | Low (smart filtering) |
| **Stationary Objects** | Invisible | Detected (if person) |
| **Speed** | Extremely Fast | Slower (requires 'inference') |
