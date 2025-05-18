
from ultralytics import YOLO
import cv2

class SurvivorDetector:
    def __init__(self, model_path='yolov8n_survivor.pt'):
        self.model = YOLO(model_path)
        self.class_id = 0  # Person class ID
    
    def process_frame(self, frame):
        results = self.model.predict(source=frame, imgsz=640, conf=0.5)
        return [obj for obj in results[0].boxes if obj.cls == self.class_id]
