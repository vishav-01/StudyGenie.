import streamlit as st
import requests
import random

# -----------------------------------------------------
# SAFETY: show errors instead of blank screen
# -----------------------------------------------------
st.set_option("client.showErrorDetails", True)

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(page_title="StudyGenie — AI Study Bestie", layout="wide")

# -----------------------------------------------------
# THEME
# -----------------------------------------------------
theme = st.sidebar.selectbox(
    "🌈 Choose Theme",
    ["Doraemon", "Sky Blue", "Pink Pastel", "Lavender"],
    index=0
)

theme_colors = {
    "Doraemon": ("#5EC2FF", "#0089E0"),
    "Sky Blue": ("#d2eaff", "#8cc8ff"),
    "Pink Pastel": ("#ffd6e8", "#ffa4c8"),
    "Lavender": ("#e7d9ff", "#c7a4ff"),
}
grad_start, grad_end = theme_colors[theme]

st.markdown(
    f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, {grad_start}, {grad_end}); }}
    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.45);
        backdrop-filter: blur(6px);
    }}
    html, body {{ font-family: Poppins, sans-serif; }}
    .question-box {{
        padding: 18px; background: #fff; border-radius: 16px; font-size: 18px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------
with st.sidebar:
    st.title("😘 StudyGenie 💖")
    tool = st.radio(
        "Choose a Tool ✨",
        [
            "AI Doubt Solver",
            "Notes Generator",
            "Summary Maker",
            "Timetable Builder",
            "Motivation Booster",
            "Flashcards",
            "Brain-Dump Cleaner",
            "Answer Checker",
            "AI Planner",
            "Mindset Reset",
            "Study Routine Designer",
            "Exam Strategy Maker",
            "Personal Study Coach",
            "Mini IQ Test Game 🧠"
        ]
    )

# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------------------------
# MOCK AI (ALWAYS WORKS)
# -----------------------------------------------------
def mock_ai(prompt: str) -> str:
    return (
        "✨ **Mock AI Response (Demo Mode)**\n\n"
        f"Tool context received:\n> {prompt}\n\n"
        "This is a safe fallback so the app NEVER blanks out.\n"
        "Add your Gemini key in secrets to enable live AI."
    )

# -----------------------------------------------------
# GEMINI (SAFE + FALLBACK)
# -----------------------------------------------------
def ask_ai(prompt: str) -> str:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return mock_ai(prompt)

    try:
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-1.0-pro:generateContent"
            f"?key={api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()

        candidates = data.get("candidates", [])
        if not candidates:
            return mock_ai(prompt)

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts or "text" not in parts[0]:
            return mock_ai(prompt)

        return parts[0]["text"]

    except Exception:
        return mock_ai(prompt)

# -----------------------------------------------------
# MAIN UI (TOOLS)
# -----------------------------------------------------
if tool != "Mini IQ Test Game 🧠":
    st.markdown(f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>", unsafe_allow_html=True)

    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['you']}")
        st.markdown(f"**Genie:** {chat['ai']}")

    prompt = st.text_area("Type your message 💬")

    if st.button("Send 💌"):
        if prompt.strip():
            reply = ask_ai(f"{tool}: {prompt}")
            st.session_state.chat_history.append({"you": prompt, "ai": reply})
            st.rerun()

    if st.button("Clear Chat 🧹"):
        st.session_state.chat_history = []
        st.rerun()

# -----------------------------------------------------
# MINI IQ GAME
# -----------------------------------------------------
if tool == "Mini IQ Test Game 🧠":
    st.markdown("<h1 style='text-align:center;'>🧠 Mini IQ Test</h1>", unsafe_allow_html=True)

    questions = [
        ("2, 6, 12, 20, 30, ?", ["36", "40", "42", "44"], "42"),
        ("Odd one out?", ["Cat", "Dog", "Lion", "Wolf"], "Cat"),
        ("A, D, G, J, M, ?", ["N", "O", "P", "Q"], "P"),
        ("Which is larger?", ["3/7", "4/9"], "4/9"),
        ("45% of 200?", ["70", "80", "90", "100"], "90"),
    ]

    if "q" not in st.session_state:
        st.session_state.q = random.choice(questions)

    q, options, ans = st.session_state.q
    st.markdown(f"<div class='question-box'>{q}</div>", unsafe_allow_html=True)
    choice = st.radio("Choose:", options)

    if st.button("Submit"):
        if choice == ans:
            st.success("🔥 Correct! Big brain energy 💙")
        else:
            st.error(f"❌ Wrong! Answer: {ans}")

    if st.button("Next Question"):
        st.session_state.q = random.choice(questions)
        st.rerun()