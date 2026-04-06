import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": " I review my notes within a day after they were taken.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I write down the main ideas from class instead of recording every single word. ",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I may keep up with the lecture without losing the important parts.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I write down questions that I want to answer later.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I use my notes to summarize the lesson in my own words.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I use headings, bullets, numbering, or similar structure in my notes.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I leave space in my notes to add missing details later.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I use symbols, abbreviations, or shorthand consistently.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I can quickly find important information in my notes when I study.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I highlight or mark the most important concepts in a useful way.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I compare my notes with lecture slides, textbooks, or class materials after class.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I add examples or explanations that help me understand the topic better.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I connect new ideas in my notes to previous knowledge.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I avoid copying everything word-for-word and focus on meaning.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " My notes help me see how different concepts are related.",
    "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I can remember key concepts from my notes without rereading everything.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " My notes help me answer quiz or exam questions.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " I feel confident studying from my notes alone.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " My note-taking method still works when the lecture is fast-paced.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": " After reviewing my notes, I feel the material stays in memory longer.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]}
]

psych_states = {
    "Excellent note-taking; very high retention": (0, 16),
    "Strong note-taking; good retention": (17, 32),
    "Moderate note-taking; mixed retention": (33, 48),
    "Weak note-taking; low retention": (49, 64),
    "Very weak note-taking; very low retention and a need to improve the method": (65, 80),
    
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Student Psychological Survey")
st.title("📝 Student Psychological Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
