import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import json
# Load the trained model
model = tf.keras.models.load_model('autism_behavior_cnn_model.keras')

# filepath: c:\ASD_Detection_Project\test_model.py

with open("class_names.json", "r") as f:
    class_names = json.load(f)
# Path to test images
test_folder = "test_images" 

# Loop over each image in the folder 
for filename in os.listdir(test_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(test_folder, filename)

        # Load and preprocess the image
        img = image.load_img(img_path, target_size=(128, 128))  # resize to model input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Predict
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions)]

        # Show image + result
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"{filename}\nPredicted: {predicted_class}")
        plt.show()

        # Print confidence
        print(f"\n🔍 {filename} — Prediction: {predicted_class}")
        for i, class_name in enumerate(class_names):
            print(f"   {class_name}: {predictions[0][i]*100:.2f}%")
        print("\n" + "-"*50)
        print(f"\n {filename} - Predicti ")



        
# import tensorflow as tf
# import numpy as np
# import os
# from tensorflow.keras.preprocessing import image
# import matplotlib.pyplot as plt

# # ✅ Load the trained model (trained on exactly 2 classes: head_banging, spinning)
# model = tf.keras.models.load_model('autism_behavior_cnn_model.keras')

# # ✅ Correct class names in the SAME ORDER used during training
# # class_names = ['head_banging', 'spinning']  # DO NOT shuffle this order

# # ✅ Path to folder containing test images
# test_folder = "test_images"

# # ✅ Loop through each image in test folder
# for filename in os.listdir(test_folder):
#     if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#         img_path = os.path.join(test_folder, filename)

#         # Preprocess image
#         img = image.load_img(img_path, target_size=(128, 128))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.0  # Normalize like in training

#         # Predict
#         predictions = model.predict(img_array)
#         predicted_index = np.argmax(predictions)
#         predicted_class = class_names[predicted_index]

#         # Show the image with prediction
#         plt.imshow(img)
#         plt.axis('off')
#         plt.title(f"{filename}\nPredicted: {predicted_class}")
#         plt.show()

#         # Print class-wise probabilities
#         print(f"\n🔍 {filename} — Predicted: {predicted_class}")
#         for i, class_name in enumerate(class_names):
#             print(f"   {class_name}: {predictions[0][i]*100:.2f}%")
#         print("\n" + "-"*50)
