import os
import numpy as np
import cv2
from flask import Flask, render_template, request
import tensorflow as tf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your model from saved_model.pb folder
model = tf.keras.models.load_model("asd_bilstm_model.h5")

def extract_frames(video_path, img_size=(64, 64), frame_skip=5):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_skip == 0:
            frame = cv2.resize(frame, img_size) / 255.0
            frames.append(frame)
        frame_count += 1
    cap.release()
    return np.array(frames)

def create_video_sequences(frames, sequence_length=10):
    sequences = []
    for i in range(len(frames) - sequence_length + 1):
        sequences.append(frames[i : i + sequence_length])
    return np.array(sequences)

def predict_video(video_path):
    frames = extract_frames(video_path)
    if len(frames) < 10:
        return "Video too short"
    sequences = create_video_sequences(frames)
    sequences_reshaped = sequences.reshape(sequences.shape[0], sequences.shape[1], -1)
    predictions = model.predict(sequences_reshaped)
    avg_prediction = np.mean(predictions)
    return "autistic" if avg_prediction >= 0.5 else "non_autistic"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    filename = None
    if request.method == "POST":
        file = request.files["video"]
        if file and file.filename != "":
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            result = predict_video(filepath)
            filename = file.filename
    return render_template("index.html", result=result, filename=filename)

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    questions = [
        "Does the child avoid eye contact?",
        "Does the child repeat phrases or actions?",
        "Does the child have difficulty with social interactions?"
    ]
    answers = []
    level = None

    if request.method == "POST":
        for i in range(len(questions)):
            answers.append(request.form.get(f"q{i}"))
        score = sum([1 for ans in answers if ans == "yes"])
        if score == 0:
            level = "Mild"
        elif score == 1:
            level = "Moderate"
        else:
            level = "Severe"
        return render_template("chatbot.html", level=level, submitted=True)

    return render_template("chatbot.html", questions=questions, submitted=False)

if __name__ == "__main__":
    app.run(debug=True)
