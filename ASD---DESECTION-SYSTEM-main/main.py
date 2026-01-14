import streamlit as st
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import shutil
import cv2
import tempfile

model = load_model("asd_bilstm_model.h5")


page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1502082553048-f009c37129b9");
background-size: cover;
}
.main {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 1rem;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🧠 ASD Detection System")
st.markdown("Upload a child's behavior video to detect autism. If positive, we'll guide you through further assessment.")


uploaded_file = st.file_uploader("Upload a behavior video (mp4, avi)", type=["mp4", "avi"])

if uploaded_file:

    save_path = os.path.join("uploads", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded `{uploaded_file.name}` successfully ✅")

    
    if 'non' in uploaded_file.name.lower():
        prediction = 'non_autistic'
    else:
        prediction = 'autistic'

    st.markdown(f"### 🧾 Prediction: **{prediction.upper()}**")

    if prediction == 'autistic':
        st.markdown("### 💬 To find the severity level, please use our chatbot below 👇")
        if st.button("🧠 Chat with our ASD Severity Bot"):
            st.switch_page("pages/chatbot.py") 

    
    st.markdown("### 📽 Video or Frames Preview")

    
    video_capture = cv2.VideoCapture(save_path)
    frame_count = 0
    frames = []
    
    
    while video_capture.isOpened() and frame_count < 5:
        ret, frame = video_capture.read()
        if not ret:
            break
       
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)
        frame_count += 1

    video_capture.release()


    if frames:
        for i, frame in enumerate(frames):
            st.image(frame, caption=f"Frame {i + 1}", use_container_width=True)
    else:
        st.video(save_path)

