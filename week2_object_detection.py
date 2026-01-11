import cv2
from ultralytics import YOLO

def main():
    """
    Main function to run the object detection using YOLOv8.
    """
    # Initialize video capture from default camera (index 0)
    # If using a drone stream, replace 0 with the RTSP/UDP URL
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    # Load the YOLOv8 Nano model
    # This will automatically download 'yolov8n.pt' if not present
    print("Loading YOLOv8 model... (this might take a moment)")
    model = YOLO('yolov8n.pt')

    print("Starting Aerial Watch (Week 2)...")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Run inference on the frame
        # stream=True is recommended for video sources to manage memory better
        results = model(frame, stream=True)

        # Process results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class ID
                cls_id = int(box.cls[0])
                
                # Get confidence score
                conf = float(box.conf[0])

                # Get class name
                name = model.names[cls_id]

                # Filter Logic: Check if it's a Person and confidence > 0.5
                if name == 'person' and conf > 0.5:
                    # Get bounding box coordinates
                    # xyxy format: x1, y1, x2, y2
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Draw Red Box around the person (BGR: 0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    # Add label text
                    label = f"{name} {conf:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Aerial Watch - Object Detection', frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
