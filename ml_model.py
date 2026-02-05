"""
UrbanEyes 24 - Deep Learning Module
Uses YOLOv8 for accurate object detection combined with Computer Vision.
"""
import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
import os
from ultralytics import YOLO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UrbanIssueDetector:
    """
    Advanced detector using YOLOv8 + Computer Vision.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the detector.
        Args:
            model_path: Path to custom YOLO model (default: yolov8n.pt)
        """
        try:
            # Use 'yolov8n.pt' (Nano) for speed. It will download automatically.
            self.model_name = model_path if model_path else 'yolov8n.pt'
            logger.info(f"Loading YOLO model: {self.model_name}")
            self.model = YOLO(self.model_name)
            self.using_deep_learning = True
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            logger.warning("Falling back to pure Computer Vision mode.")
            self.model = None
            self.using_deep_learning = False
        
        # Mapping COCO classes to our issues (Proxy logic)
        # COCO classes: https://docs.ultralytics.com/datasets/detect/coco/#dataset-classes
        self.garbage_classes = [
            # Litter (Food/Containers)
            39, 40, 41, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 
            # bottle, wine glass, cup, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake
            
            # Illegal Dumping (Furniture/Appliances/Electronics)
            56, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
            # chair, couch, potted plant, bed, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator
            
            # General Clutter/Trash
            44, 45, 73, 74, 75, 76, 77, 78, 79
            # spoon, bowl, book, clock, vase, scissors, teddy bear, hair drier, toothbrush
        ]
        
        # CV Parameters (Fallback / Hybrid)
        self.params = {
            'pothole': {
                'min_area': 500,
                'max_area': 50000,
                'min_circularity': 0.1,
                'max_circularity': 0.8,
            },
            'streetlight': {
                'night_threshold': 60,
            }
        }

    def detect_issues(self, video_path: str, debug_output: Optional[str] = None) -> Dict[str, bool]:
        """
        Analyze video for all supported issues using Hybrid Approach.
        Args:
            video_path: Path to input video
            debug_output: Optional path to save an annotated frame (e.g., 'debug.jpg')
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        detections = {
            'potholes': 0,
            'broken_streetlights': 0,
            'garbage_dumping': 0,
            'drainage_issues': 0
        }
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        skip_frames = max(1, int(fps / 2)) # Process 2 frames/sec
        
        frame_count = 0
        analyzed_frames = 0
        saved_debug = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % skip_frames != 0:
                continue
            
            analyzed_frames += 1
            
            # Resize for speed
            h, w = frame.shape[:2]
            scale = 640 / w
            frame_resized = cv2.resize(frame, (640, int(h * scale)))
            
            # Create a debug copy if we haven't saved one yet and debug_output is requested
            debug_frame = frame_resized.copy() if debug_output and not saved_debug else None
            
            # 1. Deep Learning Detection (YOLO)
            yolo_results = []
            if self.using_deep_learning:
                # Run YOLO inference
                results = self.model(frame_resized, verbose=False, conf=0.25)
                
                # Check for Garbage (Bottles, Cups, Trash items)
                has_garbage = False
                for r in results:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        if cls_id in self.garbage_classes:
                            has_garbage = True
                            if debug_frame is not None:
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cv2.rectangle(debug_frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
                                cv2.putText(debug_frame, "Garbage", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
                
                if has_garbage:
                    detections['garbage_dumping'] += 1

            # 2. Computer Vision Detection (For Potholes & Infrastructure)
            # (YOLO doesn't natively support Potholes without training)
            
            if self.detect_potholes_cv(frame_resized, debug_frame):
                detections['potholes'] += 1
                
            if self.detect_broken_streetlights_cv(frame_resized, debug_frame):
                detections['broken_streetlights'] += 1
                
            if self.detect_drainage_issues_cv(frame_resized, debug_frame):
                detections['drainage_issues'] += 1
            
            # Save the first frame that has ANY detection
            if debug_output and not saved_debug:
                # Check if current frame has detections
                current_has_detection = (
                    (detections['garbage_dumping'] > 0 and has_garbage) or
                    detections['potholes'] > 0 or # Simplified check (accumulated)
                    detections['drainage_issues'] > 0
                )
                # Or just save the first analyzed frame to show we are processing
                # Better: Save the frame if it has *new* detections or just periodically?
                # For simplicity in this verification task, save the first processed frame
                cv2.imwrite(debug_output, debug_frame)
                saved_debug = True
                
            if analyzed_frames > 200: # Limit analysis duration
                break
                
        cap.release()
        
        if analyzed_frames == 0:
            return {k: False for k in detections}
            
        # Final Decision Logic
        # Require higher confidence for CV-only detections
        results = {
            'potholes': (detections['potholes'] / analyzed_frames) > 0.10, # >10% of frames
            'broken_streetlights': (detections['broken_streetlights'] / analyzed_frames) > 0.3,
            'garbage_dumping': (detections['garbage_dumping'] / analyzed_frames) > 0.05, # YOLO is precise, so low threshold is OK
            'drainage_issues': (detections['drainage_issues'] / analyzed_frames) > 0.15
        }
        
        logger.info(f"Analysis Results: {results} (Frames: {analyzed_frames})")
        return results

    def detect_potholes_cv(self, frame: np.ndarray, debug_frame: Optional[np.ndarray] = None) -> bool:
        """
        Improved CV for Potholes:
        Finds dark, irregular shapes on the road surface.
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Blur to remove noise
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            
            # Adaptive Thresholding to find dark spots relative to surroundings
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY_INV, 15, 4
            )
            
            # Morphological Cleanup
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            
            contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detected = False
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < self.params['pothole']['min_area'] or area > self.params['pothole']['max_area']:
                    continue
                
                # Filter by circularity (Potholes are roughly circular but irregular)
                perimeter = cv2.arcLength(cnt, True)
                if perimeter == 0: continue
                circularity = 4 * np.pi * area / (perimeter ** 2)
                
                if self.params['pothole']['min_circularity'] < circularity < self.params['pothole']['max_circularity']:
                    # Location Check: Must be in lower 60% of frame (Road)
                    M = cv2.moments(cnt)
                    if M['m00'] != 0:
                        cy = int(M['m01'] / M['m00'])
                        if cy > frame.shape[0] * 0.4:
                            detected = True
                            if debug_frame is not None:
                                cv2.drawContours(debug_frame, [cnt], -1, (0, 0, 255), 2)
                                cv2.putText(debug_frame, "Pothole", (int(M['m10']/M['m00']), cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return detected
        except Exception:
            return False

    def detect_broken_streetlights_cv(self, frame: np.ndarray, debug_frame: Optional[np.ndarray] = None) -> bool:
        """
        Night Mode Detection.
        If scene is dark (Night) AND no bright light sources are found -> Broken Lights.
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            
            # If not night, return False (Assumption: Lights are off during day)
            if mean_brightness > self.params['streetlight']['night_threshold']:
                return False
                
            # It is night. Look for bright spots (working lights)
            _, bright_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            bright_pixels = cv2.countNonZero(bright_mask)
            
            # If almost zero bright pixels in a night scene -> Broken Lights
            if bright_pixels < 10: 
                if debug_frame is not None:
                    cv2.putText(debug_frame, "Night Mode: No Lights Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                return True
                
            return False
        except Exception:
            return False

    def detect_drainage_issues_cv(self, frame: np.ndarray, debug_frame: Optional[np.ndarray] = None) -> bool:
        """
        Detect large water puddles.
        Water is dark and reflective (smooth texture).
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h, w = gray.shape
            roi = gray[int(h*0.5):, :] # Bottom half
            
            # 1. Dark areas
            _, dark_mask = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY_INV)
            
            contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detected = False
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 1000: # Significant size
                    # Check texture (Standard Deviation)
                    mask = np.zeros_like(roi)
                    cv2.drawContours(mask, [cnt], -1, 255, -1)
                    mean, std = cv2.meanStdDev(roi, mask=mask)
                    
                    # Water is smooth (low std dev)
                    # Tightened threshold to 10 (was 15) to avoid asphalt false positives
                    if std[0][0] < 10:
                        detected = True
                        if debug_frame is not None:
                            # Adjust contour coordinates back to full frame
                            cnt_shifted = cnt.copy()
                            cnt_shifted[:, :, 1] += int(h*0.5)
                            cv2.drawContours(debug_frame, [cnt_shifted], -1, (255, 0, 0), 2)
                            cv2.putText(debug_frame, "Drainage/Water", (cnt_shifted[0][0][0], cnt_shifted[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            return detected
        except Exception:
            return False

# Wrappers
def analyze_video(video_path: str, model_path: str = None, debug_output: str = None) -> Dict[str, bool]:
    detector = UrbanIssueDetector(model_path)
    return detector.detect_issues(video_path, debug_output)

def analyze_image(image_path: str, model_path: str = None, debug_output: str = None) -> Dict[str, bool]:
    detector = UrbanIssueDetector(model_path)
    # Wrap image in list for consistency if needed, or just read it
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Debug frame
    debug_frame = frame.copy() if debug_output else None
    
    # Run detectors on single frame
    # YOLO
    garbage = False
    if detector.using_deep_learning:
        results = detector.model(frame, conf=0.25)
        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) in detector.garbage_classes:
                    garbage = True
                    if debug_frame is not None:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(debug_frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
                        cv2.putText(debug_frame, "Garbage", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
                    
    detections = {
        'potholes': detector.detect_potholes_cv(frame, debug_frame),
        'broken_streetlights': detector.detect_broken_streetlights_cv(frame, debug_frame),
        'garbage_dumping': garbage or detector.detect_issues(image_path)['garbage_dumping'] if False else garbage, # Avoid recursion loop, simpler fallback
        'drainage_issues': detector.detect_drainage_issues_cv(frame, debug_frame)
    }
    
    if debug_output:
        cv2.imwrite(debug_output, debug_frame)
        
    return detections
