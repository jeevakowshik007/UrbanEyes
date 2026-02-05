# UrbanEyes24 Troubleshooting Guide

## Issues Found and Fixed

### 1. Python Path Configuration
**Problem**: Python was not accessible from the command line.
**Solution**: Located Python installation at `C:\Users\jeeva\AppData\Local\Programs\Python\Python313\python.exe` and used the full path to run the application.

### 2. Flask Template Directory Structure
**Problem**: Flask was looking for templates in a `templates/` directory, but the HTML files were in the root directory.
**Solution**: 
- Created a `templates/` directory
- Moved `index.html` to `templates/index.html`

### 3. Function Name Mismatch
**Problem**: The application was trying to import `analyze_video_ml` but the function was named `analyze_video`.
**Solution**: Updated the import statement in `app.py`:
```python
# Before
from ml_model import analyze_video as analyze_video_ml

# After  
from ml_model import analyze_video
```

And updated the function call:
```python
# Before
results = analyze_video_ml(filepath)

# After
results = analyze_video(filepath)
```

## Current Status

✅ **Application is now working correctly!**

- Flask server runs successfully on `http://127.0.0.1:5000`
- Main page loads correctly with all HTML, CSS, and JavaScript
- Analyze endpoint responds correctly to requests
- All dependencies (Flask, OpenCV, NumPy) are installed and working

## How to Run the Application

1. Open command prompt
2. Navigate to the project directory: `cd "c:\Users\jeeva\OneDrive\Documents\urbaneyes 24"`
3. Run the application: `"C:\Users\jeeva\AppData\Local\Programs\Python\Python313\python.exe" app.py`
4. Open browser and go to: `http://127.0.0.1:5000`

## Testing the Application

The application can be tested using the provided test scripts:
- `final_test.py` - Tests the main page
- `test_analyze.py` - Tests the analyze endpoint

## Notes

- The ML model uses computer vision algorithms to detect urban issues
- The application supports both video and image uploads
- Maximum file size is 500MB
- Supported formats: MP4, AVI, MOV, MKV, WebM, JPG, JPEG, PNG, GIF, BMP
