from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import json
from ml_model import analyze_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'jpg', 'jpeg', 'png', 'gif', 'bmp'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_file():
    # Check for video file
    if 'video' in request.files and request.files['video'].filename != '':
        file = request.files['video']
        file_type = 'video'
    # Check for image file
    elif 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        file_type = 'image'
    else:
        return jsonify({'error': 'No file provided'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analyze based on file type
            if file_type == 'image':
                # Analyze image
                from ml_model import analyze_image
                results = analyze_image(filepath)
            else:
                # Analyze video
                results = analyze_video(filepath)
            
            # Clean up uploaded file after analysis (optional)
            # os.remove(filepath)
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': f'Error analyzing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
