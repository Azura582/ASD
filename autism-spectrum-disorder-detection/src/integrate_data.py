import os
import shutil

# --- Configuration ---

# 1. Path to the new folder you downloaded (the one containing '9_2_Arm Flapping_3', etc.)
#    IMPORTANT: Make sure to use forward slashes / or double backslashes \\
SOURCE_DIR = r"C:\Users\HP\Downloads\archive\train\train"

# 2. Path to your project's training data folder
DEST_DIR = "dataset/train"

# 3. This matches the new names to your folder names
#    (e.g., "Arm Flapping" from the new data will go into your "hand_flapping" folder)
CLASS_MAP = {
    "Arm Flapping": "hand_flapping",
    "Head Banging": "head_banging",
    "Spinning": "spinning"
}

# --- Main Script ---
print("🚀 Starting to integrate new dataset...")

if not os.path.exists(SOURCE_DIR):
    print(f"Error: Source directory not found at '{SOURCE_DIR}'")
    exit()

# Loop through all the folders in the new dataset (e.g., '9_2_Arm Flapping_3')
for folder_name in os.listdir(SOURCE_DIR):
    source_folder_path = os.path.join(SOURCE_DIR, folder_name)
    
    if os.path.isdir(source_folder_path):
        # Find the correct class name from the folder name
        found_class = None
        for new_name, existing_name in CLASS_MAP.items():
            if new_name in folder_name:
                found_class = existing_name
                break
        
        if found_class:
            # This is the path to your existing class folder (e.g., 'dataset/train/hand_flapping')
            dest_folder_path = os.path.join(DEST_DIR, found_class)
            
            # Create the destination folder if it doesn't exist
            os.makedirs(dest_folder_path, exist_ok=True)
            
            # Copy all image files from the source to the destination
            for filename in os.listdir(source_folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    source_file = os.path.join(source_folder_path, filename)
                    shutil.copy(source_file, dest_folder_path)
            
            print(f"Copied files from '{folder_name}' into '{found_class}'")

print("\n✅ Integration complete!")