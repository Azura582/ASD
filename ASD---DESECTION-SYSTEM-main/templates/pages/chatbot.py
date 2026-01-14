import streamlit as st

st.set_page_config(page_title="ASD Chatbot", page_icon="🤖")

st.title("🤖 ASD Chatbot & Consultation")

st.write("Please answer the following questions to help us assess behavioral patterns and provide personalized guidance.")

questions = {
    "Does the child respond when their name is called?": ["Yes", "Sometimes", "No"],
    "Does the child maintain eye contact during conversations?": ["Always", "Sometimes", "Rarely"],
    "Does the child engage in pretend play?": ["Yes", "Occasionally", "No"],
    "Does the child display repetitive behaviors (e.g., hand flapping, rocking)?": ["Never", "Sometimes", "Frequently"],
    "Does the child have difficulty understanding or expressing emotions?": ["No", "Mild", "Severe"],
    "Does the child get distressed by changes in routine?": ["No", "Sometimes", "Always"],
    "How would you describe the child’s language development?": ["Normal", "Delayed", "Non-verbal"],
    "Does the child show interest in interacting with peers?": ["Yes", "Sometimes", "Not at all"],
    "Does the child follow simple instructions (e.g., 'sit down')?": ["Yes", "Sometimes", "Rarely"],
    "Does the child demonstrate unusual responses to sensory input (e.g., avoids touch, sensitive to sound)?": ["No", "Mild", "Severe"]
}

score = 0

st.markdown("### 👇 Answer All Questions")

for q, options in questions.items():
    response = st.radio(q, options, key=q)
    if response == options[-1]:  
        score += 2
    elif response == options[1]:  
        score += 1

severity = ""
guidance = ""
report_content = ""

if score <= 5:
    severity = "🟢 Mild or No Indication of ASD"
    guidance = "✅ Your child shows mild or no signs of ASD. Encourage interactive play, reading time, and regular social engagement."
    report_content = f"""
    🧠 ASD Chatbot Consultation Report

    👦 Child's Assessment:
    - Severity Level: {severity}
    - Key Observations: The child shows no or mild signs of ASD. Encourage social activities, reading, and interactive play.

    💡 Suggestions:
    {guidance}

    🕒 Daily Routine Suggestion:
    - 8:00 AM: Wake-up & hygiene
    - 9:00 AM: Learning Activities
    - 11:00 AM: Snack & free play
    - 1:00 PM: Outdoor or physical activities
    - 3:00 PM: Interactive games or storytelling
    - 6:00 PM: Dinner and quiet time
    - 8:00 PM: Bedtime routine

    👨‍👩‍👧‍👦 Parent/Caregiver Tips:
    - Celebrate small achievements
    - Maintain consistent social routines
    - Encourage creativity with toys and games
    - Join ASD support communities

    📚 Useful Resources:
    - Autism Speaks Toolkits
    - CDC Developmental Milestones
    - Autism Parenting Magazine
    """
elif 6 <= score <= 12:
    severity = "🟡 Moderate Signs of ASD"
    guidance = "⚠️ Moderate signs detected. Consider early intervention programs, language therapy, and frequent play-based learning."
    report_content = f"""
    🧠 ASD Chatbot Consultation Report

    👦 Child's Assessment:
    - Severity Level: {severity}
    - Key Observations: The child shows moderate signs of ASD. Early intervention programs are recommended.

    💡 Suggestions:
    {guidance}

    🕒 Daily Routine Suggestion:
    - 8:00 AM: Wake-up & hygiene
    - 9:00 AM: Structured learning activities
    - 11:00 AM: Sensory and motor skills activities
    - 1:00 PM: Interactive games & social learning
    - 3:00 PM: Play-based therapy
    - 6:00 PM: Dinner and quiet time
    - 8:00 PM: Bedtime routine

    👨‍👩‍👧‍👦 Parent/Caregiver Tips:
    - Focus on language development
    - Encourage structured social interactions
    - Monitor emotional responses
    - Join therapy or support groups

    📚 Useful Resources:
    - [Autism Speaks Early Intervention](https://www.autismspeaks.org/family-services/tool-kits/early-intervention)
    - [Speech Therapy Resources](https://www.speech-language-therapy.com/)
    """
else:
    severity = "🔴 Strong Signs of ASD"
    guidance = "🚨 Strong signs detected. Please consult a developmental pediatrician. Consider starting Applied Behavior Analysis (ABA), speech therapy, and occupational therapy."
    report_content = f"""
    🧠 ASD Chatbot Consultation Report

    👦 Child's Assessment:
    - Severity Level: {severity}
    - Key Observations: The child shows strong signs of ASD. Professional intervention is highly recommended.

    💡 Suggestions:
    {guidance}

    🕒 Daily Routine Suggestion:
    - 8:00 AM: Wake-up & hygiene
    - 9:00 AM: Therapy sessions (ABA, speech)
    - 11:00 AM: Sensory integration and motor activities
    - 1:00 PM: Social skills training
    - 3:00 PM: Play-based therapy with caregivers
    - 6:00 PM: Dinner and rest
    - 8:00 PM: Bedtime routine

    👨‍👩‍👧‍👦 Parent/Caregiver Tips:
    - Seek professional help immediately
    - Consider starting Applied Behavior Analysis (ABA)
    - Explore speech therapy and occupational therapy
    - Engage in one-on-one learning sessions

    📚 Useful Resources:
    - [ABA Therapy Guide](https://www.appliedbehavioranalysisedu.org/)
    - [Speech Therapy Resources](https://www.speech-language-therapy.com/)
    - [Autism Parenting Magazine](https://www.autismparentingmagazine.com/)
    """

if st.button("Get Consultation"):
    st.subheader("🧠 Assessment Result:")
    st.success(severity)

    st.subheader("📋 Recommended Consultations:")
    st.write(guidance)

    st.subheader("🕒 Sample Daily Routine:")
    st.markdown("""
    - 8:00 AM – Wake up and hygiene routine  
    - 9:00 AM – Structured learning or therapy session  
    - 10:30 AM – Snack & free play  
    - 11:00 AM – Outdoor activity  
    - 12:30 PM – Lunch and rest  
    - 2:00 PM – Interactive games / storytelling  
    - 4:00 PM – Sensory or motor skills activities  
    - 6:00 PM – Dinner and quiet time  
    - 8:00 PM – Bedtime routine
    """)

    st.subheader("👨‍👩‍👧‍👦 Parent/Caregiver Tips:")
    st.markdown("""
    - Be patient and consistent  
    - Use simple and clear communication  
    - Encourage eye contact gently  
    - Celebrate small achievements  
    - Join ASD support communities  
    """)

    st.subheader("📚 Useful Resources:")
    st.markdown("""
    - [Autism Speaks Toolkits](https://www.autismspeaks.org/tool-kits)  
    - [CDC Developmental Milestones](https://www.cdc.gov/ncbddd/actearly/milestones/index.html)  
    - [Autism Parenting Magazine](https://www.autismparentingmagazine.com/)  
    """)

   
    st.download_button(
        label="📄 Download Consultation Report",
        data=report_content,
        file_name="asd_consultation_report.txt",
        mime="text/plain"
    )
