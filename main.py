import cv2
import time
import os
import datetime
from ultralytics import YOLO

def main():
    """
    Main function for Aerial Watch Security System.
    Integrates Object Detection, Logging, and Alerts.
    """
    # 1. Setup Environment
    # Ensure the logs directory exists
    log_dir = "Intruder_Logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created log directory: {log_dir}")

    # 2. User Input: Select Source
    print("\n=== Aerial Watch - Source Selection ===")
    print("1. Live Camera")
    print("2. Video File (from Demo Video folder)")
    choice = input("Enter your choice (1 or 2): ").strip()
    
    # 3. Load Model
    print("\nLoading System... (Model: YOLOv8 Nano)")
    model = YOLO('yolov8n.pt')
    
    # 4. Initialize Video Source
    if choice == '1':
        print("Initializing camera...")
        cap = cv2.VideoCapture(0)
        source_name = "Camera"
    elif choice == '2':
        # List available videos in Demo Video folder
        demo_folder = "Demo Video"
        if os.path.exists(demo_folder):
            video_files = [f for f in os.listdir(demo_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
            if video_files:
                print(f"\nAvailable videos in '{demo_folder}':")
                for i, vf in enumerate(video_files, 1):
                    print(f"  {i}. {vf}")
                video_choice = input(f"Select video (1-{len(video_files)}): ").strip()
                try:
                    video_index = int(video_choice) - 1
                    if 0 <= video_index < len(video_files):
                        video_path = os.path.join(demo_folder, video_files[video_index])
                        print(f"Loading video: {video_path}")
                        cap = cv2.VideoCapture(video_path)
                        source_name = f"Video: {video_files[video_index]}"
                    else:
                        print("Invalid selection. Exiting.")
                        return
                except ValueError:
                    print("Invalid input. Exiting.")
                    return
            else:
                print(f"No video files found in '{demo_folder}'. Exiting.")
                return
        else:
            print(f"Folder '{demo_folder}' not found. Exiting.")
            return
    else:
        print("Invalid choice. Exiting.")
        return
    
    if not cap.isOpened():
        print(f"Error: Could not open {source_name}.")
        return

    # 3. System Variables
    last_snapshot_time = 0
    cooldown_seconds = 5
    
    # For FPS calculation
    prev_frame_time = 0
    new_frame_time = 0

    print("System ARMED. Press 'q' to quit.")

    while True:
        # Read Frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = new_frame_time

        # Run Inference
        # verbose=False keeps the terminal clean
        results = model(frame, stream=True, verbose=False)

        intruder_detected = False

        # Process Detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]

                # Security Logic: Only look for 'person' with high confidence
                if name == 'person' and conf > 0.5:
                    intruder_detected = True
                    
                    # Draw Red Box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    
                    # Draw Label
                    label = f"INTRUDER {conf:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 4. Alert & Snapshots Logic
        if intruder_detected:
            # Visual Alert on Screen
            cv2.putText(frame, "STATUS: INTRUDER DETECTED", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # Automatic Snapshot with Cooldown
            current_time = time.time()
            if current_time - last_snapshot_time > cooldown_seconds:
                # Generate filename: intruder_YYYY-MM-DD_HH-MM-SS.jpg
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{log_dir}/intruder_{timestamp}.jpg"
                
                # Save the frame
                cv2.imwrite(filename, frame)
                print(f"ALARM: Snapshot saved to {filename}")
                
                # Update timer
                last_snapshot_time = current_time
        else:
            # visual status green
            cv2.putText(frame, "STATUS: MONITORING", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show FPS (Bottom left)
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(frame, fps_text, (20, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display Frame
        cv2.imshow('Aerial Watch - Security System', frame)

        # Quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
