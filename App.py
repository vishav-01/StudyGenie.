import streamlit as st
import requests
import random

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="StudyGenie — AI Study Bestie",
    layout="wide"
)

# =====================================================
# THEME SYSTEM
# =====================================================
theme = st.sidebar.selectbox(
    "🌈 Choose Theme",
    ["Doraemon", "Sky Blue", "Pink Pastel", "Lavender"],
    index=0
)

theme_colors = {
    "Doraemon": ("#5EC2FF", "#0089E0"),
    "Sky Blue": ("#d2eaff", "#8cc8ff"),
    "Pink Pastel": ("#ffd6e8", "#ffa4c8"),
    "Lavender": ("#e7d9ff", "#c7a4ff")
}

grad_start, grad_end = theme_colors[theme]

# =====================================================
# CSS
# =====================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {grad_start}, {grad_end});
        color: black;
    }}
    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.35);
        backdrop-filter: blur(6px);
    }}
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}
    .question-box {{
        padding: 20px;
        background: white;
        border-radius: 18px;
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
    st.title("😘 StudyGenie — Your AI Bestie 💖")
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

# =====================================================
# SESSION STATE
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# =====================================================
# GEMINI AI FUNCTION
# =====================================================
def ask_ai(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-1.5-flash:generateContent"
        f"?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.65,
            "topP": 0.9,
            "maxOutputTokens": 3000
        }
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        data = r.json()

        if "candidates" not in data:
            return "⚠️ Genie is tired bestie 😭"

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        st.session_state.chat_history.append(
            {"you": prompt, "ai": reply}
        )
        st.session_state.clear_input = True
        return reply

    except Exception as e:
        return f"❌ Error: {e}"

# =====================================================
# NORMAL TOOLS
# =====================================================
if tool != "Mini IQ Test Game 🧠":

    st.markdown(
        f"<h1 style='text-align:center;'>✨ {tool} ✨</h1>",
        unsafe_allow_html=True
    )

    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['you']}")
        st.markdown(f"**Genie:** {chat['ai']}")

    text_value = "" if st.session_state.clear_input else st.session_state.last_prompt
    prompt = st.text_area("Type your message 💬", value=text_value)
    st.session_state.last_prompt = prompt

    if st.button("Send 💌"):
        if prompt.strip():
            response = ask_ai(f"{tool}: {prompt}")
            st.markdown(f"**Genie:** {response}")
            st.session_state.last_prompt = ""

    if st.button("Clear Chat History 🧹"):
        st.session_state.chat_history = []
        st.session_state.last_prompt = ""
        st.session_state.clear_input = True
        st.rerun()

# =====================================================
# MINI IQ TEST GAME
# =====================================================
if tool == "Mini IQ Test Game 🧠":

    st.markdown(
        "<h1 style='text-align:center;'>🧠 Mini IQ Test</h1>",
        unsafe_allow_html=True
    )

    iq_mcq = [
        ("What number comes next? 2, 6, 12, 20, 30, __",
         ["36", "40", "42", "44"], "42"),
        ("Which one is different?",
         ["Cat", "Dog", "Lion", "Wolf"], "Cat"),
        ("ALL roses are flowers. SOME flowers fade quickly.",
         ["All roses fade quickly", "Some roses may fade quickly", "No roses fade quickly"],
         "Some roses may fade quickly"),
        ("A, D, G, J, M, __",
         ["N", "O", "P", "Q"], "P"),
        ("Odd one out: 27, 64, 125, 144, 216",
         ["27", "64", "144", "216"], "144"),
        ("Which is larger?",
         ["3/7", "4/9"], "4/9"),
        ("(3×4)² ÷ 6 =",
         ["12", "24", "36", "48"], "24"),
        ("Sun : Day :: Moon : __",
         ["Light", "Sky", "Night", "Dark"], "Night"),
        ("Which weighs more?",
         ["1 kg iron", "1 kg cotton", "Same"], "Same"),
        ("45% of 200 =",
         ["70", "80", "90", "100"], "90")
    ]

    if "current_q" not in st.session_state:
        st.session_state.current_q = random.choice(iq_mcq)

    q, options, ans = st.session_state.current_q

    st.markdown(
        f"<div class='question-box'>{q}</div>",
        unsafe_allow_html=True
    )

    choice = st.radio("Choose one:", options)

    if st.button("Submit Answer ✅"):
        if choice == ans:
            st.success("🔥 Correct bestie!! Big brain energy 💙")
        else:
            st.error(f"😭 Wrong… Correct answer: **{ans}**")

    if st.button("Next Question ➡️"):
        st.session_state.current_q = random.choice(iq_mcq)
        st.rerun()