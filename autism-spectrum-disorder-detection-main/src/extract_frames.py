import cv2
import os

# --- Configuration ---
VIDEO_SOURCE_DIR = "video_dataset"  # Folder with 'train' and 'val' subfolders of videos
FRAME_DEST_DIR = "dataset"          # Main folder to save the extracted frames
FRAMES_PER_VIDEO = 40               # How many frames to extract from each video

def extract_and_save_frames(video_path, dest_folder, video_filename):
    """Extracts a fixed number of frames spread evenly across a single video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    # Ensure we don't try to extract more frames than available
    num_to_extract = min(FRAMES_PER_VIDEO, total_frames)
    if num_to_extract == 0:
        print(f"Warning: Video {video_path} has 0 frames.")
        return

    # Calculate which frames to capture for an even spread
    frame_indices = [int(i * total_frames / num_to_extract) for i in range(num_to_extract)]

    cap = cv2.VideoCapture(video_path)
    for i, frame_index in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if ret:
            # Create a unique filename for each frame
            base_filename = os.path.splitext(video_filename)[0]
            frame_filename = f"{base_filename}_frame_{i}.jpg"
            save_path = os.path.join(dest_folder, frame_filename)
            cv2.imwrite(save_path, frame)
    cap.release()

# --- Main Script Execution ---
print("Starting frame extraction...")

# Loop through 'train' and 'val' sets
for set_name in ['train', 'val']:
    video_set_path = os.path.join(VIDEO_SOURCE_DIR, set_name)
    frame_set_path = os.path.join(FRAME_DEST_DIR, set_name)

    # Loop through class folders ('head_banging', etc.)
    for class_name in os.listdir(video_set_path):
        video_class_path = os.path.join(video_set_path, class_name)
        frame_class_path = os.path.join(frame_set_path, class_name)
        os.makedirs(frame_class_path, exist_ok=True) # Create destination folder

        if not os.path.isdir(video_class_path):
            continue

        print(f"-> Processing: {set_name}/{class_name}")
        # Loop through each video file
        for video_filename in os.listdir(video_class_path):
            video_filepath = os.path.join(video_class_path, video_filename)
            extract_and_save_frames(video_filepath, frame_class_path, video_filename)

print("\n m=nmFrame extraction complete.")





# import numpy as np
# import os
# from tensorflow.keras.preprocessing import image
# import matplotlib.pyplot as plt

# # Load the trained model (only 2 output neurons)
# model = tf.keras.models.load_model('autism_behavior_cnn_model.keras')

# # Class labels
# class_names = ['head_banging', 'spinning']

# # Path to test images
# test_folder = "test_images"

# for filename in os.listdir(test_folder):
#     if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#         img_path = os.path.join(test_folder, filename)

#         # Load and preprocess image
#         img = image.load_img(img_path, target_size=(128, 128))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.0

#         # Predict
#         predictions = model.predict(img_array)
#         predicted_index = np.argmax(predictions)
#         predicted_class = class_names[predicted_index]

#         # Show image + result
#         plt.imshow(img)
#         plt.axis('off')
#         plt.title(f"{filename}\nPredicted: {predicted_class}")
#         plt.show()

#         # Print confidence
#         print(f"\n🔍 {filename} — Prediction: {predicted_class}")
#         for i, class_name in enumerate(class_names):
#             print(f"   {class_name}: {predictions[0][i]*100:.2f}%")
#         print("\n" + "-"*50)