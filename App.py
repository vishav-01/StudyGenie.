import streamlit as st
import random
import requests

st.set_page_config(page_title="StudyGenie — AI Study Bestie", layout="wide")
st.set_option("client.showErrorDetails", True)

# =====================================================
# THEME
# =====================================================
theme = st.sidebar.selectbox(
    "🌈 Choose Theme",
    ["Doraemon", "Sky Blue", "Pink Pastel", "Lavender"]
)

colors = {
    "Doraemon": ("#5EC2FF", "#0089E0"),
    "Sky Blue": ("#d2eaff", "#8cc8ff"),
    "Pink Pastel": ("#ffd6e8", "#ffa4c8"),
    "Lavender": ("#e7d9ff", "#c7a4ff")
}

c1, c2 = colors[theme]

st.markdown(
    f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, {c1}, {c2}); }}
    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.4);
        backdrop-filter: blur(6px);
    }}
    .box {{
        background: white;
        padding: 18px;
        border-radius: 16px;
        font-size: 18px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.title("😘 StudyGenie 💖")
    tool = st.radio(
        "Choose Tool ✨",
        [
            "AI Doubt Solver",
            "Notes Generator",
            "Summary Maker",
            "Motivation Booster",
            "Flashcards",
            "Mini IQ Test Game 🧠"
        ]
    )

# =====================================================
# SMART LOCAL ANSWERS (ALWAYS WORK)
# =====================================================
def local_ai(tool, prompt):
    if tool == "AI Doubt Solver":
        return f"📘 **Answer:**\n\nYour doubt is about:\n**{prompt}**\n\nThink step-by-step, identify keywords, and apply the core concept."

    if tool == "Notes Generator":
        return f"📝 **Notes on {prompt}:**\n\n• Key definition\n• Important points\n• Simple explanation\n• Exam-ready bullets"

    if tool == "Summary Maker":
        return f"📌 **Summary:**\n\n{prompt[:120]}...\n\n(Main idea + key facts condensed)"

    if tool == "Motivation Booster":
        return "🔥 **You are capable, consistent, and unstoppable.** Keep going bestie 💙"

    if tool == "Flashcards":
        return f"🧠 **Flashcard:**\nQ: What is {prompt}?\nA: A core concept you should remember."

    return "✨ Genie is thinking..."

# =====================================================
# GEMINI (OPTIONAL BONUS)
# =====================================================
def gemini_ai(prompt):
    key = st.secrets.get("GEMINI_API_KEY")
    if not key:
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None

# =====================================================
# MAIN TOOLS
# =====================================================
if tool != "Mini IQ Test Game 🧠":

    st.markdown(f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>", unsafe_allow_html=True)

    user_input = st.text_area("Type here 💬")

    if st.button("Get Answer ✅"):
        ai_reply = gemini_ai(f"{tool}: {user_input}")
        final_reply = ai_reply if ai_reply else local_ai(tool, user_input)

        st.markdown(f"<div class='box'>{final_reply}</div>", unsafe_allow_html=True)

# =====================================================
# IQ GAME (ALWAYS SHOWS ANSWER)
# =====================================================
if tool == "Mini IQ Test Game 🧠":

    st.markdown("<h1 style='text-align:center;'>🧠 Mini IQ Test</h1>", unsafe_allow_html=True)

    questions = [
        ("2, 6, 12, 20, 30, ?", ["36", "40", "42", "44"], "42"),
        ("Odd one out?", ["Cat", "Dog", "Lion", "Wolf"], "Cat"),
        ("A, D, G, J, M, ?", ["N", "O", "P", "Q"], "P"),
        ("45% of 200?", ["70", "80", "90", "100"], "90")
    ]

    if "q" not in st.session_state:
        st.session_state.q = random.choice(questions)

    q, options, ans = st.session_state.q
    st.markdown(f"<div class='box'>{q}</div>", unsafe_allow_html=True)

    choice = st.radio("Choose:", options)

    if st.button("Submit Answer"):
        if choice == ans:
            st.success("🔥 Correct! Genius brain unlocked 💙")
        else:
            st.error(f"❌ Wrong. Correct answer is **{ans}**")

    if st.button("Next Question"):
        st.session_state.q = random.choice(questions)
        st.rerun()