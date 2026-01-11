import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# --- PAGE CONFIG ---
st.set_page_config(page_title="Industrial AI Quiz Portal", layout="centered")

# --- GOOGLE SHEETS CONNECTION ---
# Replace the URL below with your actual Google Sheet URL
# Note: In a live app, you'd put this in .streamlit/secrets.toml
url = "YOUR_GOOGLE_SHEET_URL_HERE"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FULL 90-QUESTION BANK (Abbreviated for display) ---
# [The 90 questions from the previous code block go here]
questions_bank = [
    {"q": "What does OEE stand for?", "a": "Overall Equipment Effectiveness", "options": ["Overall Equipment Effectiveness", "Optimal Energy Efficiency", "Operational Engine Error"]},
    # ... (Include all 90 questions here)
]

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["User Login", "Admin Dashboard"])

    if choice == "User Login":
        st.header("🎓 Industrial Knowledge Quiz")
        name = st.text_input("Enter Full Name")
        uid = st.text_input("Enter Login ID")

        if st.button("Start Quiz"):
            if name and uid:
                st.session_state.user = {"name": name, "id": uid}
                st.session_state.current_quiz = random.sample(questions_bank, 15)
                st.session_state.step = "quiz_active"
                st.rerun()
            else:
                st.warning("Please fill in both name and ID.")

    elif choice == "Admin Dashboard":
        st.header("🔐 Admin Dashboard")
        password = st.text_input("Admin Password", type="password")
        if password == "admin123":
            # Fetch data from Google Sheets
            data = conn.read(spreadsheet=url)
            st.dataframe(data)
            
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("Download Full Report", csv, "final_results.csv", "text/csv")

    # --- QUIZ INTERFACE ---
    if 'step' in st.session_state and st.session_state.step == "quiz_active":
        with st.form("quiz_form"):
            responses = []
            for i, item in enumerate(st.session_state.current_quiz):
                st.write(f"**Q{i+1}: {item['q']}**")
                choice = st.radio("Select answer:", item['options'], key=f"q_{i}")
                responses.append(choice)
            
            if st.form_submit_button("Submit Exam"):
                score = 0
                for i, item in enumerate(st.session_state.current_quiz):
                    if responses[i] == item['a']:
                        score += 1
                
                # Create result row
                new_data = pd.DataFrame([{
                    "Name": st.session_state.user['name'],
                    "ID": st.session_state.user['id'],
                    "Score": f"{score}/15",
                    "Percentage": f"{(score/15)*100:.1f}%",
                    "Time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                }])

                # Append to Google Sheet
                existing_data = conn.read(spreadsheet=url)
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(spreadsheet=url, data=updated_df)
                
                st.success(f"Exam Finished! Your Score: {score}/15. Data saved to cloud.")
                st.session_state.step = "done"

if __name__ == "__main__":
    main()
