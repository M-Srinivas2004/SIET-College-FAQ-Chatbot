import json
import os
import re

import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = "college_faq.csv"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.50

LANGUAGE_LABELS = ["English", "Telugu"]
TELUGU_QUESTION_MAP = {
    "కాలం": "what are the college timings",
    "సమయం": "what are the college timings",
    "అడ్మిషన్": "how can I get admission",
    "చేరడం": "how can I get admission",
    "హాస్టల్": "is hostel facility available",
    "లైబ్రరీ": "what are the library timings",
    "రవాణా": "does the college provide transportation",
    "ప్లేస్‌మెంట్": "does the college provide placements",
    "ప్లేస్మెంట్": "does the college provide placements",
    "డిపార్ట్మెంట్": "which departments are available",
    "సివిల్": "which departments are available",
    "కంప్యూటర్": "is CSE available",
    "ai": "is AI and ML available",
    "ml": "is AI and ML available",
    "శిక్షణ": "does the college provide placements",
    "వెబ్‌సైట్": "what is the official college website",
}

TELUGU_TRANSLATIONS = {
    "The college timings are from 9:10 AM to 4:00 PM.": "కళాశాల సమయం 9:10 AM నుండి 4:00 PM వరకు ఉంది.",
    "The college starts at 9:10 AM.": "కళాశాల 9:10 AM తో ప్రారంభమవుతుంది.",
    "The college closes at 4:00 PM.": "కళాశాల 4:00 PM వద్ద ముగుస్తుంది.",
    "Yes, girls' hostel facility is available.": "అవును, బాలికల హాస్టల్ సౌకర్యం అందుబాటులో ఉంది.",
    "The college website is https://sriniet.edu.in/.": "కళాశాల వెబ్‌సైట్ https://sriniet.edu.in/.",
    "The college offers Artificial Intelligence & Machine Learning (AI & ML), Computer Science Engineering (CSE), Electronics & Communication Engineering (ECE), Electrical & Electronics Engineering (EEE), Civil Engineering, and Mechanical Engineering.": "కళాశాలలో Artificial Intelligence & Machine Learning (AI & ML), Computer Science Engineering (CSE), Electronics & Communication Engineering (ECE), Electrical & Electronics Engineering (EEE), Civil Engineering మరియు Mechanical Engineering ఉన్నత విద్యా విభాగాలు ఉన్నాయి.",
    "Yes, the college offers the Artificial Intelligence & Machine Learning (AI & ML) department.": "అవును, కళాశాలలో Artificial Intelligence & Machine Learning (AI & ML) విభాగం అందుబాటులో ఉంది.",
    "The CSE management admission fee is ₹1,00,000.": "CSE మేనేజ్మెంట్ అడ్మిషన్ ఫీజు ₹1,00,000.",
    "The AI & ML management admission fee is ₹1,30,000.": "AI & ML మేనేజ్మెంట్ అడ్మిషన్ ఫీజు ₹1,30,000.",
    "Yes, the college provides transportation facilities.": "అవును, కళాశాల రవాణా సౌకర్యాన్ని అందిస్తుంది.",
    "Yes, the college provides placement facilities.": "అవును, కళాశాల ప్లేస్‌మెంట్ సౌకర్యాన్ని అందిస్తుంది.",
    "Yes, the college has a library facility.": "అవును, కళాశాలకు లైబ్రరీ సౌకర్యం ఉంది.",
    "I’m sorry, I don't have reliable information about that. Please contact the college authorities for further information.": "నాకు ఆ సమాచారం సరిగ్గా అందుబాటులో లేదు. మరిన్ని వివరాల కోసం కళాశాల అధికారులను సంప్రదించండి.",
}


def translate_to_telugu(text):
    """Translate common FAQ answers into Telugu for a better demo experience."""
    if not text:
        return text
    return TELUGU_TRANSLATIONS.get(text, text)


def normalize_telugu_question(question):
    """Map common Telugu FAQ requests to an equivalent English question."""
    normalized = question.lower().strip()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    for keyword, english_question in TELUGU_QUESTION_MAP.items():
        if keyword in normalized:
            return english_question

    return normalized


@st.cache_resource
def load_model():
    """Load the sentence-transformer model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


@st.cache_data
def load_faq_data():
    """Load the FAQ dataset from the CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), DATA_FILE)
    return pd.read_csv(file_path)


@st.cache_data
def prepare_embeddings():
    """Create sentence embeddings for each FAQ question."""
    faq_df = load_faq_data()
    model = load_model()
    questions = faq_df["question"].fillna("").astype(str).tolist()
    embeddings = model.encode(questions, convert_to_numpy=True)
    return faq_df, embeddings


def find_best_match(question, faq_df, faq_embeddings, model):
    """Return the closest FAQ entry based on semantic similarity."""
    if not question or not question.strip():
        return None, 0.0

    query_embedding = model.encode([question.strip()], convert_to_numpy=True)
    similarity_scores = cosine_similarity(query_embedding, faq_embeddings)[0]
    best_index = int(np.argmax(similarity_scores))
    best_score = float(similarity_scores[best_index])

    if best_score >= SIMILARITY_THRESHOLD:
        return faq_df.iloc[best_index], best_score

    return None, best_score


def get_bot_reply(user_question, language="English"):
    """Generate a chatbot answer for the user question in the chosen language."""
    question_for_match = user_question
    if language == "Telugu":
        question_for_match = normalize_telugu_question(user_question)

    faq_df, faq_embeddings = prepare_embeddings()
    model = load_model()
    match, score = find_best_match(question_for_match, faq_df, faq_embeddings, model)

    if match is not None:
        answer = match["answer"]
        if language == "Telugu":
            answer = translate_to_telugu(answer)
        return answer, score

    fallback = (
        "I’m sorry, I don't have reliable information about that. "
        "Please contact the college authorities for further information."
    )
    if language == "Telugu":
        fallback = "నాకు ఆ సమాచారం సరిగ్గా అందుబాటులో లేదు. మరిన్ని వివరాల కోసం కళాశాల అధికారులను సంప్రదించండి."
    return fallback, score


st.set_page_config(page_title="SIET College FAQ Chatbot", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
        .stApp { background: linear-gradient(135deg, #07111d 0%, #0b1d32 30%, #11294a 100%); }
        div[data-testid="stChatMessage"] { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; }
        [data-testid="stSidebar"] { background: rgba(7,17,29,0.9); }
        .stButton > button { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "language" not in st.session_state:
    st.session_state.language = "English"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

st.title("🎓 SIET College FAQ Chatbot")
st.subheader("Srinivasa Institute of Engineering and Technology")

welcome_message = (
    "Hello! 👋 I am the SIET College FAQ Assistant. Ask me anything about departments, admissions, timings, hostel, library, transportation, placements, and other college facilities."
)
if st.session_state.language == "Telugu":
    welcome_message = "హలో! 👋 నేను SIET కాలేజ్ FAQ అసిస్టెంట్. డిపార్ట్మెంట్లు, అడ్మిషన్, సమయం, హాస్టల్, లైబ్రరీ, రవాణా, ప్లేస్‌మెంట్ గురించి ప్రశ్నలు అడగండి."

st.write(welcome_message)

faq_df, _ = prepare_embeddings()
category_list = faq_df["category"].dropna().unique().tolist()

with st.sidebar:
    st.markdown("### Language")
    st.session_state.language = st.selectbox(
        "Choose language",
        LANGUAGE_LABELS,
        index=LANGUAGE_LABELS.index(st.session_state.language),
        key="lang_select",
    )

    st.markdown("---")
    st.markdown("### Quick FAQ Categories")
    for category in category_list:
        st.markdown(f"- {category.title()}")

    st.markdown("---")
    st.markdown("### College Snapshot")
    st.write("- College Name: Srinivasa Institute of Engineering and Technology")
    st.write("- Website: https://sriniet.edu.in/")
    st.write("- Timings: 9:10 AM to 4:00 PM")
    st.write("- Campus Facilities: Library, transport, placements, hostel")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.last_answer = ""

quick_questions = [
    "What are the college timings?",
    "Which departments are available?",
    "How can I get admission?",
    "Does the college provide transportation?",
]
if st.session_state.language == "Telugu":
    quick_questions = [
        "కళాశాల సమయం ఎంత?",
        "డిపార్ట్మెంట్లు ఏవి?",
        "చేరడం ఎలా ఉంటుంది?",
        "కళాశాల రవాణా అందిస్తుందా?",
    ]

cols = st.columns(len(quick_questions))
for index, question in enumerate(quick_questions):
    if cols[index].button(question, key=f"quick_{index}"):
        st.session_state.chat_history.append(("user", question))
        reply, score = get_bot_reply(question, st.session_state.language)
        st.session_state.chat_history.append(("assistant", reply))
        st.session_state.last_answer = reply

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

user_question = st.chat_input("Ask a question about the college...")

if user_question is not None:
    trimmed_question = user_question.strip()
    if trimmed_question == "":
        st.warning("Please enter a valid question.")
    else:
        st.session_state.chat_history.append(("user", trimmed_question))
        with st.chat_message("user"):
            st.write(trimmed_question)

        reply, similarity_score = get_bot_reply(trimmed_question, st.session_state.language)
        st.session_state.chat_history.append(("assistant", reply))
        st.session_state.last_answer = reply

        with st.chat_message("assistant"):
            st.write(reply)
            if similarity_score < SIMILARITY_THRESHOLD:
                st.caption("No confident match found in the FAQ knowledge base.")

if st.session_state.last_answer:
    voice_payload = json.dumps(st.session_state.last_answer)
    voice_html = f"""
    <div style="margin-top: 14px; margin-bottom: 8px;">
        <button onclick="speakText()" style="padding: 10px 16px; border-radius: 12px; border: none; background: linear-gradient(135deg, #7c3aed, #00c2ff); color: white; font-weight: 600; cursor:pointer;">🔊 Listen to answer</button>
    </div>
    <script>
        const answerText = {voice_payload};
        function speakText() {{
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance(answerText);
                utterance.lang = 'en-US';
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert('Speech synthesis is not supported in this browser.');
            }}
        }}
    </script>
    """
    st.components.v1.html(voice_html, height=110)

st.markdown("---")
st.subheader("FAQ Highlights")

highlight_columns = [
    ("Admissions", "Students can contact the college authorities or apply through EAMCET/AP EAPCET and ECET as applicable."),
    ("Departments", "AI & ML, CSE, ECE, EEE, Civil, and Mechanical Engineering programs are available."),
    ("Fees", "Management fees are ₹1,30,000 for AI & ML and ₹1,00,000 for CSE."),
    ("Facilities", "The college provides library, transport, placements, and girls' hostel facilities."),
]

columns = st.columns(len(highlight_columns))
for idx, (title, text) in enumerate(highlight_columns):
    with columns[idx]:
        st.markdown(f"### {title}")
        st.write(text)
