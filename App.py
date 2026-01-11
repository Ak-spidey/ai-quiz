import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION & MOCK DATA ---
# In a real app, use a database. Here we use session_state for demo.
if 'results_db' not in st.session_state:
    st.session_state.results_db = []

# Mock Question Bank (Expand this to 90+ questions for 6 sets)
questions_bank = [
    {"q": "What does OEE stand for?", "a": "Overall Equipment Effectiveness", "options": ["Overall Equipment Effectiveness", "Optimal Energy Efficiency", "Operational Engine Error"], "cat": "Production"},
    {"q": "Formula for Productivity?", "a": "Output / Input", "options": ["Output / Input", "Input / Output", "Sales - Cost"], "cat": "Formula"},
    {"q": "Which sensor detects metal without contact?", "a": "Inductive Proximity", "options": ["Inductive Proximity", "Capacitive", "Photoelectric"], "cat": "Sensors"},
    # ... add more questions here
]

# --- APP LOGIC ---
def main():
    st.title("🏭 Industrial AI Quiz Portal")

    # Sidebar Navigation
    menu = ["User Login", "Admin Dashboard"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "User Login":
        st.subheader("Student Login")
        name = st.text_input("Full Name")
        login_id = st.text_input("Employee/Student ID")

        if st.button("Start Quiz"):
            if name and login_id:
                st.session_state.user = {"name": name, "id": login_id}
                # Randomly pick 15 questions for this session
                st.session_state.current_quiz = random.sample(questions_bank, min(len(questions_bank), 15))
                st.session_state.step = "testing"
            else:
                st.error("Please enter details")

    elif choice == "Admin Dashboard":
        st.subheader("Admin Access")
        pw = st.text_input("Admin Password", type="password")
        if pw == "admin123":
            st.success("Access Granted")
            if st.session_state.results_db:
                df = pd.DataFrame(st.session_state.results_db)
                st.write("### All User Scores")
                st.table(df)
            else:
                st.info("No records found yet.")

    # --- QUIZ INTERFACE ---
    if 'step' in st.session_state and st.session_state.step == "testing":
        with st.form("quiz_form"):
            user_answers = []
            for i, q in enumerate(st.session_state.current_quiz):
                ans = st.radio(f"Q{i+1}: {q['q']}", q['options'], key=f"q{i}")
                user_answers.append(ans)
            
            if st.form_submit_button("Submit Quiz"):
                score = 0
                for i, q in enumerate(st.session_state.current_quiz):
                    if user_answers[i] == q['a']:
                        score += 1
                
                # Show Result
                st.balloons()
                st.markdown(f"## Your Score: {score}/15")
                
                # Save to "Database"
                st.session_state.results_db.append({
                    "Name": st.session_state.user['name'],
                    "ID": st.session_state.user['id'],
                    "Score": score,
                    "Timestamp": pd.Timestamp.now()
                })
                st.session_state.step = "finished"

if __name__ == "__main__":
    main()