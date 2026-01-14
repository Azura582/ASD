import cv2
import os
import shutil
import numpy as np

# --- Configuration ---
# You'll need to adjust these thresholds based on your images
BLUR_THRESHOLD = 35.0   # Lower is more blurry. Start with 35 and adjust.
DARKNESS_THRESHOLD = 50 # Lower is darker (0-255). 50 is a good starting point.

SOURCE_DIR = "dataset" # The folder with your 'train' and 'val' sets
BAD_QUALITY_DIR = "dataset_bad_quality" # Where bad images will be moved

# --- Main Logic ---

def check_image_quality(image_path):
    """Checks a single image for blur and darkness."""
    image = cv2.imread(image_path)
    if image is None:
        return False, "Could not read image"

    # 1. Check for blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    focus_measure = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 2. Check for darkness
    brightness = np.mean(image)

    if focus_measure < BLUR_THRESHOLD:
        return False, f"Blurry (Score: {focus_measure:.2f})"
    
    if brightness < DARKNESS_THRESHOLD:
        return False, f"Too Dark (Brightness: {brightness:.2f})"
        
    return True, "Good Quality"

# --- Script Execution ---
print("🚀 Starting dataset cleaning...")
os.makedirs(BAD_QUALITY_DIR, exist_ok=True)

# Walk through the train and val directories
for dirpath, dirnames, filenames in os.walk(SOURCE_DIR):
    for filename in filenames:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(dirpath, filename)
            
            is_good, reason = check_image_quality(image_path)
            
            if not is_good:
                print(f"Flagged: {image_path} - Reason: {reason}")
                
                # Move the bad image
                destination_path = os.path.join(BAD_QUALITY_DIR, filename)
                shutil.move(image_path, destination_path)

print("\n✅ Cleaning complete. Bad images moved to 'dataset_bad_quality'.")