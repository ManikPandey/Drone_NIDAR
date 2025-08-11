import torch
import numpy as np
import cv2

class SurvivorDetector:
    """
    Handles survivor detection using a YOLOv8 model. This class loads the model
    and provides a method to detect people in an image frame.
    """
    def __init__(self, model_path='yolov8n.pt', confidence_threshold=0.65):
        """
        Initializes the SurvivorDetector.

        Args:
            model_path (str): Path to the YOLOv8 model file (.pt).
            confidence_threshold (float): Min confidence score for a valid detection.
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"[VISION] Initializing YOLOv8 on device: '{self.device}'")
        self.conf = confidence_threshold
        
        try:
            # Use the official ultralytics library to load the model
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            print("[VISION] YOLO model loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load YOLO model: {e}")
            self.model = None

    def detect(self, frame: np.ndarray) -> list:
        """
        Performs inference on a single frame to detect survivors (persons).

        Args:
            frame (np.ndarray): The image frame from a video stream (BGR format).

        Returns:
            list: A list of detections. Each detection is a dictionary with
                  'box': [x1, y1, x2, y2] and 'confidence': score.
        """
        if self.model is None:
            return []

        # Perform inference. The model handles color conversion.
        results = self.model(frame, verbose=False) # verbose=False for cleaner output
        
        detections = []
        # Process results object
        for result in results:
            for box in result.boxes:
                # We only care about the 'person' class, which is index 0
                if int(box.cls[0]) == 0 and float(box.conf[0]) > self.conf:
                    detections.append({
                        'box': [int(coord) for coord in box.xyxy[0]],
                        'confidence': float(box.conf[0])
                    })
        return detections

# Example usage for testing this module independently
if __name__ == '__main__':
    print("Running a test detection on a sample image...")
    # You should replace this with a path to a real test image
    # e.g., test_image = cv2.imread('path/to/survivor_image.jpg')
    test_image = np.zeros((480, 640, 3), dtype=np.uint8) # Dummy black image

    # Initialize detector
    detector = SurvivorDetector()

    if detector.model and test_image is not None:
        survivors = detector.detect(test_image)
        if survivors:
            print(f"Detected {len(survivors)} survivor(s).")
            for s in survivors:
                print(f"  - BBox: {s['box']}, Confidence: {s['confidence']:.2f}")
        else:
            print("No survivors detected in the sample image.")