# UrbanEyes24 Detection Accuracy Improvements

## Major Code Refactoring (2025-02-02)

The `ml_model.py` module has been completely rewritten to improve accuracy, code quality, and maintainability.

### 1. Advanced Computer Vision Algorithms
We have moved away from simple thresholding to more robust feature detection:

*   **Pothole Detection**:
    *   **Old**: Simple area check.
    *   **New**: Adaptive Thresholding + Convexity Defects + Circularity Analysis + Location Filtering (Road Area). This drastically reduces false positives from shadows.
*   **Broken Streetlights**:
    *   **Old**: Looked for dark spots in the sky.
    *   **New**: "Night Mode" detection. Checks if the scene is dark (night) and then scans for bright spots. If no bright spots are found in a night scene, it flags a potential issue.
*   **Garbage Dumping**:
    *   **Old**: Basic color check.
    *   **New**: Texture Entropy + Color Saturation Variance. Garbage is typically messy and colorful. We now check for high-texture areas that are also colorful.
*   **Drainage Issues**:
    *   **Old**: Dark area check.
    *   **New**: Surface Reflection Analysis. Water is flat and reflective. We check for large dark areas with low texture variance (smoothness) compared to the surrounding road.

### 2. Object-Oriented Design
*   Introduced `UrbanIssueDetector` class for better state management.
*   Parameters are now configurable in a dictionary, making it easier to tune without changing code logic.
*   Added `logging` for better debugging.

### 3. Dynamic Thresholding
*   Instead of hardcoded values (e.g., `pixel < 50`), algorithms now use statistical properties of the image (e.g., `pixel < mean * 0.6`). This makes the model work better in different lighting conditions (sunny vs. cloudy).

### 4. Preparation for Deep Learning
*   The code is structured to easily plug in a YOLO/Deep Learning model in the future.
*   The `UrbanIssueDetector` class can be extended to load a `.pt` or `.weights` file.

## How to Verify
Run the verification script to see the model in action on sample files:
```bash
python verify_model.py
```

## Next Steps for "Pro" Accuracy
To achieve human-level accuracy, we recommend training a Custom YOLO model:
1.  Collect 500+ images of local potholes/garbage.
2.  Label them using a tool like LabelImg.
3.  Train YOLOv8 on this dataset.
4.  Update `ml_model.py` to load this model.
