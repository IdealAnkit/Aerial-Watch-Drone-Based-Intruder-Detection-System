from flask import Flask, render_template, Response, request, jsonify
import cv2
import time
import os
import datetime
from ultralytics import YOLO
import threading

app = Flask(__name__)

# Global variables
camera = None
model = None
is_running = False
source_type = "camera"
video_path = None
last_snapshot_time = 0
cooldown_seconds = 5
detection_status = "Monitoring"

def init_model():
    """Initialize YOLO model"""
    global model
    if model is None:
        model = YOLO('yolov8n.pt')
    return model

def get_video_source():
    """Get video source based on current settings"""
    global camera, source_type, video_path
    
    if camera is not None:
        camera.release()
    
    if source_type == "camera":
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(video_path)
    
    return camera

def generate_frames():
    """Generate video frames with detection - continuously running"""
    global camera, model, is_running, last_snapshot_time, detection_status
    
    # Ensure log directory exists
    log_dir = "Intruder_Logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Initialize model once
    model = init_model()
    
    prev_frame_time = 0
    
    # Keep the stream alive continuously
    while True:
        # Wait until system is started
        if not is_running:
            # Send a blank frame while waiting
            blank_frame = (b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n'
                          b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
                          b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c'
                          b'\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\xff\xd9\r\n')
            yield blank_frame
            time.sleep(0.1)
            continue
        
        # Check if camera exists and is opened
        if camera is None or not camera.isOpened():
            time.sleep(0.1)
            continue
            
        success, frame = camera.read()
        if not success:
            time.sleep(0.1)
            continue
        
        # Calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = new_frame_time
        
        # Run detection
        results = model(frame, stream=True, verbose=False)
        intruder_detected = False
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]
                
                if name == 'person' and conf > 0.5:
                    intruder_detected = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    label = f"INTRUDER {conf:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Status overlay
        if intruder_detected:
            detection_status = "INTRUDER DETECTED"
            cv2.putText(frame, "STATUS: INTRUDER DETECTED", (20, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # Snapshot with cooldown
            current_time = time.time()
            if current_time - last_snapshot_time > cooldown_seconds:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{log_dir}/intruder_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                last_snapshot_time = current_time
        else:
            detection_status = "Monitoring"
            cv2.putText(frame, "STATUS: MONITORING", (20, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # FPS overlay
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(frame, fps_text, (20, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Main page"""
    # Get available videos
    demo_folder = "Demo Video"
    video_files = []
    if os.path.exists(demo_folder):
        video_files = [f for f in os.listdir(demo_folder) 
                      if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    # Get recent snapshots
    log_dir = "Intruder_Logs"
    snapshots = []
    if os.path.exists(log_dir):
        files = sorted([f for f in os.listdir(log_dir) if f.endswith('.jpg')], reverse=True)
        snapshots = files[:6]  # Last 6 snapshots
    
    return render_template('index.html', 
                         video_files=video_files, 
                         snapshots=snapshots,
                         is_running=is_running)

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start():
    """Start detection"""
    global is_running, source_type, video_path, camera
    
    data = request.json
    source_type = data.get('source', 'camera')
    video_file = data.get('video_path', None)
    
    print(f"[DEBUG] Starting with source_type: {source_type}, video_file: {video_file}")
    
    if source_type == "video" and video_file:
        video_path = os.path.join("Demo Video", video_file)
        print(f"[DEBUG] Full video path: {video_path}")
        print(f"[DEBUG] File exists: {os.path.exists(video_path)}")
    else:
        video_path = None
    
    camera = get_video_source()
    
    if camera is not None and camera.isOpened():
        is_running = True
        print(f"[DEBUG] Camera opened successfully!")
        return jsonify({'status': 'started', 'source': source_type})
    else:
        print(f"[DEBUG] Failed to open camera/video")
        return jsonify({'status': 'error', 'message': 'Failed to open video source'}), 500

@app.route('/stop', methods=['POST'])
def stop():
    """Stop detection"""
    global is_running, camera
    
    is_running = False
    if camera is not None:
        camera.release()
        camera = None
    
    return jsonify({'status': 'stopped'})

@app.route('/status')
def status():
    """Get current status"""
    return jsonify({
        'is_running': is_running,
        'detection_status': detection_status
    })

@app.route('/snapshots')
def get_snapshots():
    """Get list of recent snapshots"""
    log_dir = "Intruder_Logs"
    snapshots = []
    if os.path.exists(log_dir):
        files = sorted([f for f in os.listdir(log_dir) if f.endswith('.jpg')], reverse=True)
        snapshots = files[:6]  # Last 6 snapshots
    return jsonify({'snapshots': snapshots})

@app.route('/snapshot/<filename>')
def serve_snapshot(filename):
    """Serve a snapshot image"""
    log_dir = "Intruder_Logs"
    from flask import send_from_directory
    return send_from_directory(log_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
