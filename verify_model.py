import os
import glob
from ml_model import analyze_image, analyze_video

def test_model():
    print("Starting comprehensive model verification...")
    
    # Create debug output directory
    debug_dir = os.path.join('static', 'debug_output')
    os.makedirs(debug_dir, exist_ok=True)
    
    uploads_dir = 'uploads'
    files = glob.glob(os.path.join(uploads_dir, '*'))
    
    print(f"{'File':<40} | {'Potholes':<10} | {'Lights':<10} | {'Garbage':<10} | {'Drainage':<10}")
    print("-" * 95)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        ext = filename.split('.')[-1].lower()
        
        debug_path = os.path.join(debug_dir, f"debug_{filename}.jpg") # Add .jpg even for video (it's a frame)
        
        results = {}
        try:
            if ext in ['jpg', 'jpeg', 'png', 'bmp']:
                results = analyze_image(file_path, debug_output=debug_path)
            elif ext in ['mp4', 'avi', 'mov']:
                results = analyze_video(file_path, debug_output=debug_path)
            else:
                continue
                
            # Format results
            p = "YES" if results.get('potholes') else "no"
            l = "YES" if results.get('broken_streetlights') else "no"
            g = "YES" if results.get('garbage_dumping') else "no"
            d = "YES" if results.get('drainage_issues') else "no"
            
            print(f"{filename[:40]:<40} | {p:<10} | {l:<10} | {g:<10} | {d:<10}")
            
        except Exception as e:
            print(f"{filename[:40]:<40} | ERROR: {str(e)}")

    print("-" * 95)
    print(f"Debug images saved to: {debug_dir}")

if __name__ == "__main__":
    test_model()
