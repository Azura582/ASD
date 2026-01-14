import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import json

# Set dataset paths
train_dir = 'dataset/train'
val_dir = 'dataset/val'
img_size = (128, 128)
batch_size = 32
initial_epochs = 10
fine_tune_epochs = 15 
total_epochs = initial_epochs + fine_tune_epochs

# Load class names
with open("class_names.json", "r") as f:
    class_names = json.load(f)

# Load data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir, image_size=img_size, batch_size=batch_size, shuffle=True,
    label_mode='int', class_names=class_names
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    val_dir, image_size=img_size, batch_size=batch_size, shuffle=False,
    label_mode='int', class_names=class_names
)

# Configure for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# Extract all labels from the training dataset
train_labels = np.concatenate([y for x, y in train_ds], axis=0)

# Calculate class weights to handle imbalance
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_labels),
    y=train_labels
)
class_weight_dict = dict(enumerate(class_weights))
print(" Calculated Class Weights:", class_weight_dict)

# Data augmentation layers
data_augmentation = models.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
], name="data_augmentation")

# Build model with MobileNetV2 base
IMG_SHAPE = img_size + (3,)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SHAPE,
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False # Start with the base model frozen

# Create the full model
inputs = layers.Input(shape=IMG_SHAPE)
x = data_augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(class_names), activation='softmax')(x)
model = models.Model(inputs, outputs)

# p0nl,iyz0STAGE 1: Compile and train the top layer
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("--- STAGE 1: Training classifier head ---")
history = model.fit(train_ds,
                    epochs=initial_epochs,
                    validation_data=val_ds,
                    class_weight=class_weight_dict)

#  STAGE 2: Unfreeze layers for Fine-Tuning
base_model.trainable = True6

# Fine-tune from this layer onwards
fine_tune_at = 100
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# Re-compile with a very low learning rate
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), # 10x smaller LR
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("\n--- STAGE 2: Fine-tuning the model ---")
history_fine = model.fit(train_ds,
                         epochs=total_epochs,
                         initial_epoch=history.epoch[-1], # Resume from where we left off
                         validation_data=val_ds,
                         class_weight=class_weight_dict)

# save the final fine-tuned model
model.save('autism_behavior_finetuned.keras')
print("Model saved as 'autism_behavior_finetuned.keras'")


# Visualize training for both stages
acc = history.history['accuracy'] + history_fine.history['accuracy']
val_acc = history.history['val_accuracy'] + history_fine.history['val_accuracy']
loss = history.history['loss'] + history_fine.history['loss']
val_loss = history.history['val_loss'] + history_fine.history['val_loss']

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Train Acc')
plt.plot(val_acc, label='Val Acc')
plt.plot([initial_epochs-1, initial_epochs-1], plt.ylim(), label='Start Fine-Tuning')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Train Loss')
plt.plot(val_loss, label='Val Loss')
plt.plot([initial_epochs-1, initial_epochs-1], plt.ylim(), label='Start Fine-Tuning')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')

plt.tight_layout()
plt.show()
plt


























# import tensorflow as tf
# from tensorflow.keras import layers, models
# import matplotlib.pyplot as plt
# import json

# # 📁 Set dataset paths
# train_dir = 'dataset/train'
# val_dir = 'dataset/val'
# img_size = (128, 128)
# batch_size = 32

# # 🏷️ Load class names
# with open("class_names.json", "r") as f:
#     class_names = json.load(f)

# # 📦 Load training data
# train_ds = tf.keras.preprocessing.image_dataset_from_directory(
#     train_dir,
#     image_size=img_size,
#     batch_size=batch_size,
#     shuffle=True,
#     label_mode='int',
#     class_names=class_names
# )

# # 📦 Load validation data
# val_ds = tf.keras.preprocessing.image_dataset_from_directory(
#     val_dir,
#     image_size=img_size,
#     batch_size=batch_size,
#     shuffle=False, # No need to shuffle validation data
#     label_mode='int',
#     class_names=class_names
# )

# # 🚀 Improve performance
# AUTOTUNE = tf.data.AUTOTUNE
# train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# # ✨ NEW: Add data augmentation layers
# data_augmentation = models.Sequential([
#     layers.RandomFlip("horizontal"),
#     layers.RandomRotation(0.2),
#     layers.RandomZoom(0.2),
# ], name="data_augmentation")

# # 🧠 NEW: Use MobileNetV2 for Transfer Learning
# IMG_SHAPE = img_size + (3,)
# base_model = tf.keras.applications.MobileNetV2(
#     input_shape=IMG_SHAPE,
#     include_top=False, # Do not include the final classification layer
#     weights='imagenet' # Use weights pre-trained on ImageNet
# )

# # Freeze the pre-trained model so we only train our new layers
# base_model.trainable = False

# # 🧠 NEW: Build the final model
# inputs = layers.Input(shape=IMG_SHAPE)
# x = data_augmentation(inputs) # Apply augmentation first
# x = tf.keras.applications.mobilenet_v2.preprocess_input(x) # Preprocess for MobileNetV2
# x = base_model(x, training=False) # Run the base model (frozen)
# x = layers.GlobalAveragePooling2D()(x) # Pool the features
# x = layers.Dropout(0.3)(x) # Add dropout for regularization
# outputs = layers.Dense(len(class_names), activation='softmax')(x) # Our output layer

# model = models.Model(inputs, outputs)

# # ⚙️ Compile the model
# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# model.summary()

# # 🏋️ Train the model
# history = model.fit(train_ds, validation_data=val_ds, epochs=15) # NOTE: Start with fewer epochs

# # 💾 Save model
# model.save('autism_behavior_mobilenet_v2.keras')
# print("✅ Model saved as 'autism_behavior_mobilenet_v2.keras'")

# # 📊 Visualize training
# plt.figure(figsize=(12, 5))

# # Accuracy plot
# plt.subplot(1, 2, 1)
# plt.plot(history.history['accuracy'], label='Train Acc')
# plt.plot(history.history['val_accuracy'], label='Val Acc')
# plt.title('Model Accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.legend()

# # Loss plot
# plt.subplot(1, 2, 2)
# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Val Loss')
# plt.title('Model Loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()

# plt.tight_layout()
# plt.show()





# import tensorflow as tf
# from tensorflow.keras import layers, models
# import matplotlib.pyplot as plt
# import json
# import os

# # 📁 Set dataset paths
# train_dir = 'dataset/train'
# val_dir = 'dataset/val'
# img_size = (128, 128)
# batch_size = 32

# # 🏷️ Set fixed class names — MUST match your folder names exactly
# class_names = ['head_banging', 'spinning','hand_flapping']  # DO NOT shuffle this order

# # ✅ Save class names for prediction use later
# with open("class_names.json", "w") as f:
#     json.dump(class_names, f)

# # 📦 Load training data with fixed class order
# train_ds = tf.keras.preprocessing.image_dataset_from_directory(
#     train_dir,
#     image_size=img_size,
#     batch_size=batch_size,
#     shuffle=True,
#     label_mode='int',
#     class_names=class_names
# )

# # 📦 Load validation data
# val_ds = tf.keras.preprocessing.image_dataset_from_directory(
#     val_dir,
#     image_size=img_size,
#     batch_size=batch_size,
#     shuffle=True,
#     label_mode='int',
#     class_names=class_names
# )

# print("✔️ Classes used:", class_names)

# # 🚀 Improve performance using caching and prefetching
# AUTOTUNE = tf.data.AUTOTUNE
# train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# # 🧠 Build CNN model
# model = models.Sequential([
#     layers.Rescaling(1./255, input_shape=(128, 128, 3)),
#     layers.Conv2D(32, (3, 3), activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Conv2D(128, (3, 3), activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Flatten(),
#     layers.Dense(128, activation='relu'),
#     layers.Dropout(0.5),
#     layers.Dense(len(class_names), activation='softmax')  # 2 classes
# ])

# # ⚙️ Compile model
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# # 🏋️ Train the model
# history = model.fit(train_ds, validation_data=val_ds, epochs=50)

# # 💾 Save model
# model.save('autism_behavior_cnn_model.keras')
# print("✅ Model saved as 'autism_behavior_cnn_model.keras'")

# # 📊 Visualize training
# plt.figure(figsize=(12, 5))

# # Accuracy plot
# plt.subplot(1, 2, 1)
# plt.plot(history.history['accuracy'], label='Train Acc')
# plt.plot(history.history['val_accuracy'], label='Val Acc')
# plt.title('Model Accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.legend()

# # Loss plot
# plt.subplot(1, 2, 2)
# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Val Loss')
# plt.title('Model Loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend()

# plt.tight_layout()
# plt.show()
