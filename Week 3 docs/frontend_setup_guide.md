# Frontend Setup Guide - Web Interface

This guide explains how to run the professional web-based frontend for Aerial Watch.

## What You Get

A complete web interface with:
- **Live Video Streaming** via browser (MJPEG)
- **Start/Stop Controls** - No command line needed
- **Source Selection** - Camera or Video File
- **Real-time Alerts** - Visual status indicators
- **Auto-updating Gallery** - See new snapshots as they're captured
- **REST API** - Backend endpoints for integration

## Prerequisites
- Completed setup for Weeks 1-3
- Flask installed (`venv\Scripts\pip install flask`)
- Virtual environment activated

## Quick Start

1. **Activate Virtual Environment**:
   ```powershell
   venv\Scripts\activate
   ```

2. **Start the Web Server**:
   ```powershell
   python app.py
   ```

3. **Open Browser**:
   - Navigate to: `http://localhost:5000`
   - You'll see the Aerial Watch dashboard

## Using the Interface

### Starting Detection

1. **Select Video Source**:
   - **Live Camera**: Uses your webcam (default)
   - **Video File**: Choose from Demo Video folder

2. **Click "Start Monitoring"**:
   - Video feed appears immediately
   - Detection starts automatically
   - Status changes to "✓ Monitoring Active"

3. **Real-time Features**:
   - Green status = Normal monitoring
   - Red status = "⚠️ INTRUDER DETECTED"
   - FPS counter shows performance
   - Gallery updates every 3 seconds with new snapshots

### Stopping

- Click **"Stop"** button anytime
- Video feed stops
- Can restart with different source

### Snapshot Gallery

- Bottom section shows last 6 intruder snapshots
- **Auto-updates** while monitoring is active
- Click images to view full size
- Timestamps show when each was captured

## Technical Features

### Frontend (index.html + JavaScript)
- Responsive design (works on desktop/tablet)
- Real-time status polling (1-second intervals)
- Dynamic gallery updates (3-second intervals)
- Cache-busted video feed for smooth restarts

### Backend API Endpoints (app.py)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main page |
| `/start` | POST | Start monitoring |
| `/stop` | POST | Stop monitoring |
| `/status` | GET | Get system status |
| `/snapshots` | GET | Get snapshot list |
| `/video_feed` | GET | MJPEG stream |
| `/snapshot/<file>` | GET | Serve image |

### Video Streaming
- Uses **MJPEG** (Motion JPEG) format
- Efficient frame-by-frame streaming
- Continuous connection (survives stop/start)
- Blank frames sent when idle

## Troubleshooting

### Black Screen on Video Feed
- **Solution**: Click Stop, then Start again
- Refresh the browser page
- Check terminal for "[DEBUG]" messages

### Port 5000 Already in Use
```python
# In app.py, change the last line:
app.run(debug=True, threaded=True, port=5001)
```

### Camera Not Found
- Close other apps using webcam (Zoom, Teams, etc.)
- Check camera permissions in Windows Settings
- Try restarting the Flask server

### Video File Not Working
- Ensure `Demo Video` folder exists in project root
- Check file format: `.mp4`, `.avi`, `.mov`, or `.mkv`
- Watch terminal debug output for file path
- Verify file isn't corrupted

### Snapshots Not Updating
- Gallery auto-updates only when monitoring is **active**
- Check `Intruder_Logs` folder is being created
- Verify detections are happening (look for red boxes)

## Comparison: CLI vs Web Interface

| Feature | main.py (CLI) | app.py (Web) |
|---------|---------------|--------------|
| Interface | Terminal | Browser |
| Start/Stop | Manual restart | Button click |
| View Snapshots | File explorer | Live gallery |
| Remote Access | ❌ | ✅ (network) |
| Multi-user | ❌ | ✅ |
| API Access | ❌ | ✅ |

## Next Steps

- The web interface is production-ready for demonstrations
- Can be deployed to a server for remote monitoring
- API endpoints can be consumed by mobile apps
- Consider adding authentication for security
