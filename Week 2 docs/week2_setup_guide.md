# Week 2 Setup Guide: The "Brain" (Object Detection)

This guide covers the specific steps to set up the environment for Week 2, where we introduce Deep Learning using YOLOv8.

## Prerequisites
-   You must have completed the **Week 1 Setup** (Python installed, virtual environment created).
-   Your virtual environment should be activated.

## 1. Activate Virtual Environment (If not already active)

**Command:**
```powershell
venv\Scripts\activate
```
*(You will see `(venv)` at the start of your terminal line)*

## 2. Install YOLOv8 Dependencies

The YOLOv8 model is part of the `ultralytics` library. This is a separate package from OpenCV that we need to install.

**Command:**
```powershell
pip install ultralytics
```

**What this does:**
-   Downloads the `ultralytics` package.
-   Installs `torch` and `torchvision` (PyTorch libraries required for deep learning).
-   Installs other utilities like `pandas` and `matplotlib`.
-   *Note: This might take a minute as these are large libraries.*

## 3. The First Run (Downloading the Model)

**Command:**
```powershell
python week2_object_detection.py
```

**Important Note for First Run:**
-   When you run this script for the very first time, you will see a message:
    `Downloading https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt to 'yolov8n.pt' ...`
-   **Do not close the terminal.** The code is automatically downloading the pre-trained "brain" (weights file) execution.
-   This only happens once. Future runs will be instant.

## 4. Troubleshooting

-   **"Module not found: ultralytics"**: This means you didn't install the library **inside** your virtual environment. Make sure you see `(venv)` or use `venv\Scripts\pip install ultralytics`.
-   **Laggy Video**: Object detection requires heavy math.
    -   On a generic laptop CPU, you might get 5-10 FPS (Frames Per Second).
    -   This is normal! We are using the "Nano" (`yolov8n`) model to keep it as fast as possible.
