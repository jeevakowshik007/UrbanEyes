# UrbanEyes24 - Urban Infrastructure Analysis System

A web application that uses ML to analyze videos and detect urban infrastructure issues including:
- 🕳️ Potholes
- 💡 Broken Streetlights
- 🗑️ Illegal Garbage Dumping
- 🌊 Drainage Issues

## Features

- Simple video upload interface
- Real-time video analysis
- Clear results display
- Modern, responsive UI

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Access the Application

Open your browser and navigate to: `http://localhost:5000`

## ML Model Integration

The ML model is already integrated into the application. To use your trained model:

1. **Update `ml_model.py`**: Replace the placeholder methods in the `UrbanIssueDetector` class with your actual ML model inference code.

2. **Load your model**: Update the `__init__` method to load your trained model file.

3. **Implement detection methods**: Complete the `detect_potholes()`, `detect_broken_streetlights()`, `detect_garbage_dumping()`, and `detect_drainage_issues()` methods with your model's inference logic.

The application will automatically use your ML model once implemented in `ml_model.py`.

## Project Structure

```
urbaneyes24/
├── app.py              # Flask backend application
├── ml_model.py         # ML model integration module
├── index.html          # Main upload page
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── static/
│   ├── style.css      # Styling
│   └── script.js      # Frontend JavaScript
└── uploads/           # Uploaded videos (created automatically)
```

## Next Steps

1. Train your ML model for detecting the four types of issues
2. Complete the implementation in `ml_model.py` with your actual model inference code
3. Add video preprocessing if needed (frame extraction, resizing, etc.)
4. Consider adding progress tracking for long videos
5. Add database to store analysis history

## Notes

- Maximum video file size: 500MB
- Supported formats: MP4, AVI, MOV, MKV, WebM
- Videos are stored in the `uploads/` directory

