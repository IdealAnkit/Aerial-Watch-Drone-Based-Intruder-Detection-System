import cv2
import numpy as np

def main():
    """
    Main function to run the motion detection.
    """
    # Initialize video capture from default camera (index 0)
    # If using a drone stream, replace 0 with the RTSP/UDP URL
    cap = cv2.VideoCapture(0)
    
    # Initialize background subtractor
    # MOG2 is a Gaussian Mixture-based Background/Foreground Segmentation Algorithm
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    print("Starting Aerial Watch (Week 1)...")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Apply background subtraction to get the foreground mask
        fg_mask = back_sub.apply(frame)

        # Clean up the mask: remove shadows (which are usually gray in MOG2)
        # Thresholding ensures we only get the moving objects (white)
        # 254 is a safe threshold to remove shadows (usually 127)
        _, fg_mask_clean = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
        
        # Optional: Morphological operations to remove noise (small white dots)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask_clean = cv2.morphologyEx(fg_mask_clean, cv2.MORPH_OPEN, kernel)

        # Find contours on the mask
        contours, _ = cv2.findContours(fg_mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filter out small movements/noise based on area
            if cv2.contourArea(contour) < 500:
                continue

            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw green rectangle around the object
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Aerial Watch - Motion Detection', frame)
        
        # Also show the mask for understanding what the computer sees
        # cv2.imshow('Foreground Mask', fg_mask_clean)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
