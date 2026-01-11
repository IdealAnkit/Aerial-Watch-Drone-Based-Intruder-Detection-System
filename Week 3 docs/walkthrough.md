# Week 1 Verification: Motion Detection

## Prerequisites
- A webcam connected to your computer.
- The Python virtual environment set up (which has been done).

## Steps to Verify

1.  **Run the Script**:
    Open a terminal in `e:\SEM 7\Antigravity Project\P01` and run:
    ```powershell
    venv\Scripts\python week1_motion_detection.py
    ```

2.  **Observe the Output**:
    - A window titled "Aerial Watch - Motion Detection" should appear showing your webcam feed.
    - **Motion Detection**: Wave your hand. You should see a green box drawn around your moving hand.
    - **Stationary Objects**: Check that stationary objects (background) do not have boxes around them.

3.  **Quit**:
    - Press the `q` key on your keyboard while the video window is focused to exit the application.

## Troubleshooting
- If the webcam doesn't open, ensure no other application is using it.
- If the green boxes are too sensitive (detecting noise), we can adjust the `contourArea` threshold in the code.

# Week 2 Verification: Object Detection

## Prerequisites
- The `ultralytics` library installed (`venv\Scripts\pip install ultralytics`).

## Steps to Verify

1.  **Run the Script**:
    ```powershell
    venv\Scripts\python week2_object_detection.py
    ```
    *Note: The first time you run this, it will download the model weights (a few MBs), so it might take a minute to start.*

2.  **Observe the Output**:
    - A window titled "Aerial Watch - Object Detection" should appear.
    - **Person Detection**: Walk into the frame. You should see a **RED** box around you with the label `person` and a confidence score (e.g., `0.85`).
    - **Filtering**: Check that other objects (chairs, cups) do NOT have red boxes around them.

3.  **Quit**:
    - Press `q` to exit.

# Week 3 Verification: The Full System

## Prerequisites
- The final script `main.py` is ready.
- Ensure you have the `Intruder_Logs` folder (the script will create it if missing).

## Steps to Verify

1.  **Run the Script**:
    ```powershell
    venv\Scripts\python main.py
    ```

2.  **Observe the Output**:
    - **Monitoring Mode**: When no one is in frame, text should say **"STATUS: MONITORING"** in Green.
    - **Intruder Mode**: Walk into frame. Text should change to **"STATUS: INTRUDER DETECTED"** in Red.

3.  **Test Snapshots & Cooldown**:
    - Triger the detection.
    - Watch the terminal. You should see `ALARM: Snapshot saved to Intruder_Logs/intruder_...`.
    - Move around for the next 5 seconds. You should **NOT** see another "Snapshot saved" message immediately (Cooldown active).
    - After 5 seconds, if you are still there, another snapshot *should* be saved.

4.  **Check Logs**:
    - Quit the app (`q`).
    - Open the `Intruder_Logs` folder in your file explorer.
    - Verify that images are saved with the correct timestamp (e.g., `intruder_2025-12-29_22-30-05.jpg`).
