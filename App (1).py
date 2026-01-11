import streamlit as st
import pandas as pd
import random

# 1. Setup Data Storage
if 'db' not in st.session_state:
    st.session_state.db = []

# 2. Question Bank (90 Questions categorized)
# I have included a sample here; you can expand this list following the same format
questions_bank = [
    {"q": "What does OEE stand for?", "a": "Overall Equipment Effectiveness", "options": ["Overall Equipment Effectiveness", "Optimal Energy Efficiency", "Operational Engine Error"]},
    {"q": "Formula for Productivity?", "a": "Output / Input", "options": ["Output / Input", "Input / Output", "Sales / Cost"]},
    {"q": "Which sensor detects metal without contact?", "a": "Inductive Proximity", "options": ["Inductive Proximity", "Capacitive", "Photoelectric"]},
    {"q": "What does JIT stand for?", "a": "Just In Time", "options": ["Just In Time", "Job In Transit", "Joint Industrial Task"]},
    {"q": "Standard voltage for industrial sensors?", "a": "24V DC", "options": ["24V DC", "230V AC", "5V DC"]},
    {"q": "What is Poka-Yoke?", "a": "Error Proofing", "options": ["Error Proofing", "Continuous Improvement", "Waste Removal"]},
    {"q": "What does NO mean in a switch?", "a": "Normally Open", "options": ["Normally Open", "Normally Off", "Next Operation"]},
    {"q": "Formula for Availability in OEE?", "a": "Operating Time / Planned Production Time", "options": ["Operating Time / Planned Production Time", "Good Pieces / Total Pieces", "Actual Speed / Design Speed"]},
    {"q": "What is a Thermocouple used for?", "a": "Temperature Measurement", "options": ["Temperature Measurement", "Pressure Sensing", "Flow Control"]},
    {"q": "What does SPC stand for?", "a": "Statistical Process Control", "options": ["Statistical Process Control", "Standard Product Cost", "Systematic Process Check"]},
    # ... (Add all 90 questions here in this format)
]

# 3. Sidebar Navigation
st.sidebar.title("Industrial Quiz Portal")
page = st.sidebar.radio("Navigation", ["User Login & Quiz", "Admin Dashboard"])

# --- USER PAGE ---
if page == "User Login & Quiz":
    st.header("📝 Candidate Examination")
    
    # Login Section
    with st.container(border=True):
        name = st.text_input("Full Name")
        login_id = st.text_input("Login ID / Employee ID")
    
    if st.button("Start Quiz"):
        if name and login_id:
            st.session_state.current_user = {"name": name, "id": login_id}
            # Shuffle and pick 15 random questions
            st.session_state.test_questions = random.sample(questions_bank, 15)
            st.session_state.quiz_started = True
        else:
            st.error("Please enter Name and ID to proceed.")

    # Quiz Section
    if st.session_state.get("quiz_started"):
        st.divider()
        with st.form("exam_form"):
            user_answers = []
            for i, item in enumerate(st.session_state.test_questions):
                st.write(f"**Q{i+1}: {item['q']}**")
                ans = st.radio("Select one:", item['options'], key=f"ans_{i}")
                user_answers.append(ans)
            
            if st.form_submit_button("Submit Final Answers"):
                # Calculate Score
                score = 0
                for i, item in enumerate(st.session_state.test_questions):
                    if user_answers[i] == item['a']:
                        score += 1
                
                # Save to "Admin Database"
                result = {
                    "Name": st.session_state.current_user['name'],
                    "ID": st.session_state.current_user['id'],
                    "Score": score,
                    "Total": 15,
                    "Percentage": f"{(score/15)*100:.1f}%",
                    "Status": "Pass" if score >= 9 else "Fail"
                }
                st.session_state.db.append(result)
                
                st.success(f"Quiz Submitted! Your Score: {score}/15")
                st.balloons()
                st.session_state.quiz_started = False

# --- ADMIN PAGE ---
elif page == "Admin Dashboard":
    st.header("🔑 Admin Control Panel")
    pw = st.text_input("Enter Admin Password", type="password")
    
    if pw == "admin789":
        st.subheader("All Student Results")
        if st.session_state.db:
            df = pd.DataFrame(st.session_state.db)
            st.table(df)
            
            # Export option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Marks Report", csv, "results.csv", "text/csv")
        else:
            st.info("No candidates have taken the test yet.")
    elif pw:
        st.error("Incorrect Password")
