import streamlit as st

st.title("🤖 ASD Severity Level Chatbot")

st.markdown("Answer the following questions to assess the level of severity:")

questions = [
    "Does the child maintain eye contact?",
    "Does the child respond to their name?",
    "Does the child show repetitive behavior?",
    "Does the child struggle with social interactions?",
    "Does the child have delayed speech or communication skills?"
]

score = 0
for q in questions:
    ans = st.radio(q, ["Yes", "No"], key=q)
    if ans == "Yes":
        score += 1

if st.button("Get Severity Level"):
    if score <= 1:
        level = "Mild"
    elif score <= 3:
        level = "Moderate"
    else:
        level = "Severe"

    st.markdown(f"### 🚨 Predicted Severity Level: **{level} Autism**")

    if level == "Severe":
        st.info("👨‍⚕️ Please consult a specialist as soon as possible.")
    else:
        st.success("✅ Consider behavioral therapy and regular assessments.")
