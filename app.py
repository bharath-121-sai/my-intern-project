import streamlit as st
import os
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from collections import Counter

from utils.pdf_utils import extract_text_from_pdf
from utils.gemini_utils import generate_summary, answer_question
from utils.history_utils import save_chat_history

# Load NLP model (spaCy for NER & keyword extraction)
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="📘 Research Paper Assistant", layout="wide")

st.title("📘 AI Research Paper Assistant")
st.markdown("Upload a research paper PDF and explore it with summaries, Q&A, and insights!")

uploaded_pdf = st.file_uploader("📂 Upload your research paper (PDF)", type=["pdf"])

if uploaded_pdf:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)

    st.success("✅ PDF extracted successfully!")

    # --- Summary Section ---
    if st.button("🧾 Generate Short Summary"):
        with st.spinner("Summarizing paper..."):
            summary = generate_summary(pdf_text + "\nMake it very short, 4-6 lines only.")
        st.subheader("📄 Summary (Short)")
        st.write(summary)
        save_chat_history("Short summary of paper", summary)

    st.markdown("---")

    # --- Q&A Section ---
    st.subheader("💬 Ask Questions from the Paper")
    user_question = st.text_input("Enter your question here:")

    if st.button("🔍 Get Short Answer"):
        with st.spinner("Analyzing paper..."):
            short_question = user_question + "\nAnswer in 2-3 concise sentences only."
            answer = answer_question(pdf_text, short_question)
        st.chat_message("user").write(user_question)
        st.chat_message("assistant").write(answer)
        save_chat_history(user_question, answer)

    st.markdown("---")

    # --- Insights Section ---
    st.subheader("📊 Research Paper Insights")

    # Word Frequency
    words = re.findall(r'\w+', pdf_text.lower())
    common_words = Counter(words).most_common(15)

    fig, ax = plt.subplots()
    ax.bar([w[0] for w in common_words], [w[1] for w in common_words])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Word Cloud
    st.subheader("☁️ Word Cloud of Paper")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(pdf_text)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

    # Named Entity Recognition (NER)
    st.subheader("🧩 Named Entities (Technologies, Orgs, Methods)")
    doc = nlp(pdf_text[:5000])  # limit for performance
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if entities:
        for ent, label in entities[:20]:
            st.write(f"**{ent}** → {label}")
    else:
        st.info("No entities detected in sample text.")

    st.markdown("---")

    # --- Download Chat History Section ---
    st.subheader("📥 Download Chat History")
    if os.path.exists("chat_history.csv"):
        with open("chat_history.csv", "rb") as file:
            st.download_button(
                label="⬇️ Download History as CSV",
                data=file,
                file_name="chat_history.csv",
                mime="text/csv"
            )
    else:
        st.info("No chat history available yet. Ask or summarize first!")

else:
    st.info("👆 Please upload a PDF to start.")
