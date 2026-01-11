# Step-by-Step Setup Guide

This guide explains every action we took to set up the "Aerial Watch" project environment. It explains the commands used and why they are necessary.

## 1. Create a Python Virtual Environment

**Command:**
```powershell
python -m venv venv
```

**Explanation:**
-   **`python -m venv`**: This tells Python to run its built-in "virtual environment" module.
-   **`venv`** (the second one): This is the name of the folder we want to create. You could name this anything (like `my_env`), but `venv` is the standard convention.
-   **Why do we do this?**
    -   It creates a "sandbox" for this specific project.
    -   If we install libraries here, they won't mess up other Python projects on your computer.
    -   It prevents version conflicts (e.g., Project A needs Library v1.0, Project B needs Library v2.0).

## 2. Activate the Virtual Environment (Windows)

**Command:**
```powershell
venv\Scripts\activate
```
*(Note: In our automated setup, we often skip this by pointing directly to the executable, e.g., `venv\Scripts\python`, but when working manually, you activate it first.)*

**Explanation:**
-   This script changes your shell's environment variables.
-   Once activated, when you type `python`, it uses the Python inside the `venv` folder, not the global system Python.
-   You will usually see `(venv)` appear at the start of your command line prompt.

## 3. Install Dependencies

**Command:**
```powershell
pip install opencv-python numpy
```
*Or if not activated:* `venv\Scripts\pip install opencv-python numpy`

**Explanation:**
-   **`pip`**: The Package Installer for Python. It downloads code from the internet (PyPI).
-   **`opencv-python`**: The main library for Computer Vision. It contains all the tools to read video, process images, and detect motion.
-   **`numpy`**: A library for math and working with arrays. OpenCV images are just big arrays of numbers, so NumPy is required to handle them efficiently.
-   **Why these two?** They are the absolute minimum requirements for our Week 1 goal (Motion Detection).

## 4. Run the Code

**Command:**
```powershell
python week1_motion_detection.py
```
*Or if not activated:* `venv\Scripts\python week1_motion_detection.py`

**Explanation:**
-   This tells the Python interpreter to read our script file and execute the instructions top-to-bottom.
-   Since we are using the `python` from our virtual environment, it has access to the `opencv-python` and `numpy` libraries we just installed.

## Summary of Workflow

1.  **Isolate**: Create a venv so we don't break things.
2.  **Equip**: Install the specific tools (libraries) we need.
3.  **Execute**: Run our custom code using those tools.
