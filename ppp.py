import streamlit as st
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import random

# Download tokenizer data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ---------- PDF Text Extraction ----------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ---------- TF-IDF Summarization ----------
def simple_summarize(text, n_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) <= n_sentences:
        return " ".join(sentences)

    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(sentences)
    scores = np.array(X.sum(axis=1)).ravel()
    top_indices = scores.argsort()[-n_sentences:][::-1]
    top_sentences = [sentences[i] for i in top_indices]
    summary = " ".join(top_sentences)

    # 🔹 Simple NLG phrasing for smoothness
    intro = random.choice([
        "In summary, this paper mainly discusses that",
        "To sum up, the research highlights that",
        "Overall, it focuses on",
        "In essence, the key idea is that"
    ])
    return f"{intro} {summary}"

# ---------- Question Answering with NLG ----------
def answer_question(text, question):
    question = question.lower()
    text_lower = text.lower()

    # 1️⃣ Rule: Handle “full form of”
    match = re.search(r'full form of ([a-zA-Z]+)', question)
    if match:
        term = match.group(1)
        pattern = re.compile(rf"{term}\s*\((.*?)\)|\b{term}\b\s+stands for\s+(.*?)\b", re.IGNORECASE)
        found = pattern.search(text)
        if found:
            expansion = found.group(1) or found.group(2)
            return f"The full form of {term.upper()} is {expansion}."

    # 2️⃣ TF-IDF based answer
    sentences = sent_tokenize(text)
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(sentences + [question])
    cosine_sim = cosine_similarity(X[-1], X[:-1])
    best_sentence_index = cosine_sim.argmax()
    best_sentence = sentences[best_sentence_index]

    # 🔹 Add natural phrasing (NLG touch)
    openers = [
        "According to the paper,",
        "The document mentions that",
        "From the research, it can be seen that",
        "Based on the content of the paper,"
    ]
    return f"{random.choice(openers)} {best_sentence.strip()}"

# ---------- Streamlit UI ----------
st.title("📘 Research Paper Assistant (Classical NLP + NLG)")
st.write("""
Upload a research paper (PDF) and this app will:
- Extract text from the paper  
- Summarize it using TF-IDF + Natural Language Generation  
- Answer questions using rules + similarity  
🧠 *(No pretrained AI models used — only classical NLP + NLG logic)*
""")

uploaded_file = st.file_uploader("📂 Upload your research paper (PDF)", type="pdf")

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF extracted successfully!")

    if st.button("🧾 Generate Summary"):
        with st.spinner("Generating summary..."):
            summary = simple_summarize(pdf_text)
        st.subheader("📄 Summary:")
        st.write(summary)

    st.subheader("💬 Ask a Question from the Paper")
    user_q = st.text_input("Enter your question:")
    if user_q:
        answer = answer_question(pdf_text, user_q)
        st.write(f"**Answer:** {answer}")
