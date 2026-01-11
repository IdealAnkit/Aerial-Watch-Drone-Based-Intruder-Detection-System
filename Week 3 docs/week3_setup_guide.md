# Week 3 Setup Guide: The "System"

This guide covers how to run the final security product.

## Prerequisites
-   Completed Week 1 & 2 Setup.
-   `ultralytics` installed.
-   `opencv-python` installed.

## 1. Activate Environment

**Command:**
```powershell
venv\Scripts\activate
```

## 2. Directory Structure

Before running, your project folder should look like this (simplified):
```text
P01/
├── venv/
├── week1_motion_detection.py
├── week2_object_detection.py
├── main.py  <-- The final file
└── yolov8n.pt (Downloaded automatically)
```

## 3. Run the System

**Command:**
```powershell
python main.py
```

## 4. What Happens Next?

1.  **Initialization**: The script will check for a folder named `Intruder_Logs`.
    -   *If missing*, it creates it.
    -   *If present*, it uses it.
2.  **Loading**: It loads YOLOv8 (taking 1-2 seconds).
3.  **Operation**:
    -   The window opens.
    -   When you walk in front of it, it saves images to `Intruder_Logs`.
    -   Check that folder to see your "caught" images!

## 5. Troubleshooting (Week 3 Specific)

-   **Permission Error**: If the script crashes saying "Permission denied" when creating logs, try running VS Code/Terminal as Administrator.
-   **Disk Space**: If you leave this running for days in a busy hallway, `Intruder_Logs` could get huge. The 5-second timer helps, but be aware!
