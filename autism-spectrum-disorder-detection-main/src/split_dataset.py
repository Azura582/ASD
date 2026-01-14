import os
import random
import shutil  
# Define paths {adjust as necessaty2} with your dictory structure  0-git git bash]r
SOURCE_DIR = "Videos"
BASE_DATA_DIR = "video_dataset" # New folder for split videos
split_ratio = 0.8

# Create destination directories
train_dir = os.path.join(BASE_DATA_DIR, "train")
val_dir = os.path.join(BASE_DATA_DIR, "val")
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Iterate over each class
for class_name in os.listdir(SOURCE_DIR):
    class_path = os.path.join(SOURCE_DIR, class_name)
    if not os.path.isdir(class_path):
        continue

    # Create class subdirectories in train and val
    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)

    # Get list of videos and shuffle them
    videos = os.listdir(class_path)
    random.shuffle(videos)

    # Split the list of videos
    split_point = int(len(videos) * split_ratio)
    train_videos = videos[:split_point]
    val_videos = videos[split_point:]

    # Copy video files to the correct sets
    for video in train_videos:
        shutil.copy(os.path.join(class_path, video), os.path.join(train_dir, class_name, video))
    for video in val_videos:
        shutil.copy(os.path.join(class_path, video), os.path.join(val_dir, class_name, video))

    print(f"Class '{class_name}': {len(train_videos)} train videos, {len(val_videos)} validation videos.")




# import os
# import shutil
# import random

# def split_dataset(source_dir, train_dir, val_dir, split_ratio=0.8):
#     os.makedirs(train_dir, exist_ok=True)
#     os.makedirs(val_dir, exist_ok=True)

#     for category in os.listdir(source_dir):
#         category_path = os.path.join(source_dir, category)
#         if not os.path.isdir(category_path):
#             continue

#         images = os.listdir(category_path)
#         random.shuffle(images)
#         split_point = int(len(images) * split_ratio)

#         train_images = images[:split_point]
#         val_images = images[split_point:]

#         os.makedirs(os.path.join(train_dir, category), exist_ok=True)
#         os.makedirs(os.path.join(val_dir, category), exist_ok=True)

#         for img in train_images:
#             shutil.copy(os.path.join(category_path, img), os.path.join(train_dir, category, img))

#         for img in val_images:
#             shutil.copy(os.path.join(category_path, img), os.path.join(val_dir, category, img))

#         print(f"Category '{category}': {len(train_images)} train, {len(val_images)} val")

# # Example usage:
# split_dataset("frames", "dataset/train", "dataset/val")
