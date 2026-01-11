# Learning Guide: Week 3 + Frontend - Complete System

This document explains both versions of the Aerial Watch system: the CLI version (`main.py`) and the web-based version (`app.py`).

## Two Versions of the System

### 1. main.py - Command Line Interface
- Traditional terminal-based application
- Interactive text menus
- Direct OpenCV window display
- Good for: Testing, development, simple deployments

### 2. app.py - Web Interface
- Modern Flask-based web application
- Browser-based controls and display
- RESTful API architecture
- Good for: Demos, remote access, production use

---

## Part A: main.py (CLI Version)

### Core Concepts

#### Source Selection with User Input
```python
print("\n=== Aerial Watch - Source Selection ===")
print("1. Live Camera")
print("2. Video File (from Demo Video folder)")
choice = input("Enter your choice (1 or 2): ").strip()
```

**Key Learning**: `input()` pauses execution and waits for user input. `.strip()` removes whitespace.

#### Video File Discovery
```python
video_files = [f for f in os.listdir(demo_folder) 
               if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
```

**List Comprehension**: Filters files by extension in one line.

---

## Part B: app.py (Web Interface)

### Flask Web Framework

#### API Endpoints
```python
@app.route('/start', methods=['POST'])
def start():
    # Handle start request
    return jsonify({'status': 'started'})
```

**Concept**: Each route is a **REST API endpoint** that browsers/apps can call.

### Video Streaming Generator

```python
def generate_frames():
    while True:
        if not is_running:
            yield blank_frame  # Keep connection alive
            continue
        
        # Process and encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
```

**Key Concepts**:
- **Generator function**: Uses `yield` instead of `return`, produces values one at a time
- **MJPEG streaming**: Sends JPEG frames continuously over HTTP
- **Infinite loop**: Keeps connection alive, adapts to start/stop states

### Frontend-Backend Communication

#### JavaScript Fetch API
```javascript
fetch('/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({source: source, video_path: videoPath})
});
```

**Flow**: Browser → JSON request → Flask → JSON response → Browser

#### Dynamic UI Updates
```javascript
setInterval(async () => {
    const response = await fetch('/status');
    const data = await response.json();
    // Update UI based on data
}, 1000);
```

**Polling**: Browser checks server status every second for real-time updates.

---

## Common Components (Both Versions)

### 1. Environment Setup
Both create the `Intruder_Logs` directory:
```python
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
```

### 2. Cooldown Timer
Both prevent snapshot spam:
```python
if current_time - last_snapshot_time > cooldown_seconds:
    # Save snapshot
    last_snapshot_time = current_time
```

### 3. Detection Logic
Both use identical YOLOv8 processing:
```python
if name == 'person' and conf > 0.5:
    intruder_detected = True
```

### 4. FPS Calculation
Both measure performance:
```python
fps = 1 / (new_frame_time - prev_frame_time)
```

---

## Key Differences

| Aspect | main.py | app.py |
|--------|---------|--------|
| **Display** | OpenCV window | Browser |
| **Control** | Keyboard ('q' to quit) | Buttons |
| **Source Selection** | Terminal menu | Dropdown |
| **Snapshot View** | File explorer | Auto-updating gallery |
| **Architecture** | Monolithic | Client-Server |
| **Global State** | Local variables | Flask global vars |
| **Concurrency** | Single thread | Multi-threaded (Flask) |

---

## Advanced Concepts in app.py

### Global Variables in Flask
```python
camera = None
is_running = False
```

**Why global?**: Multiple routes need shared state. In production, use a proper state manager.

### MJPEG Multipart Response
```python
Response(generate_frames(),
         mimetype='multipart/x-mixed-replace; boundary=frame')
```

**Format**: Special HTTP response that sends multiple JPEG images sequentially.

### Cache Busting
```javascript
videoFeed.src = '/video_feed?t=' + new Date().getTime();
```

**Why?**: Prevents browser from using cached old stream when restarting.

---

## Production Considerations

### main.py Best Practices
- ✅ Simple deployment
- ✅ No network dependencies
- ❌ Limited to local machine
- ❌ Manual intervention required

### app.py Best Practices
- ✅ Remote monitoring possible
- ✅ Multiple users can view
- ✅ API for integrations
- ❌ Needs WSGI server for production (not Flask debug mode)
- ❌ Requires proper authentication in real deployments

---

## Summary

**main.py** is perfect for learning the core detection logic and testing locally.

**app.py** demonstrates professional web development with:
1. **Backend**: Flask REST API with video streaming
2. **Frontend**: Modern UI with real-time updates
3. **Architecture**: Separation of concerns (client/server)
4. **Integration**: API-ready for mobile apps or dashboards
