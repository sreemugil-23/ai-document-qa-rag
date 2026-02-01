import streamlit as st
import os
import hashlib

from app.pdf_loader import load_pdf_text
from app.rag import answer_question

# ----------------------------------
# Streamlit page config
# ----------------------------------
st.set_page_config(page_title="AI Document Q&A", layout="centered")

st.title("📄 ENAKKU ELLAMEY THERIYUM")
st.write("Upload a PDF and ask questions grounded in the document.")

# ----------------------------------
# Session state initialization
# ----------------------------------
if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

if "last_pdf_hash" not in st.session_state:
    st.session_state.last_pdf_hash = None

# ----------------------------------
# Helper: cache path from file hash
# ----------------------------------


def get_cache_path(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    return f"data/cache/{file_hash}.pkl", file_hash


# ----------------------------------
# PDF upload
# ----------------------------------
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    os.makedirs("data/docs", exist_ok=True)
    os.makedirs("data/cache", exist_ok=True)

    pdf_path = os.path.join("data/docs", uploaded_file.name)

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    cache_path, pdf_hash = get_cache_path(pdf_path)

    # NEW PDF → reset vectors
    if st.session_state.last_pdf_hash != pdf_hash:
        st.session_state.vector_ready = False
        st.session_state.last_pdf_hash = pdf_hash

    st.success("PDF uploaded successfully ✅")

    # ----------------------------------
    # Read PDF ONCE
    # ----------------------------------
    with st.spinner("Reading PDF..."):
        document = load_pdf_text(pdf_path)

    # ----------------------------------
    # Question input
    # ----------------------------------
    question = st.text_input("Ask a question about the document")

    if question:
        with st.spinner("Thinking..."):
            answer, context, evaluation = answer_question(
                document=document,
                question=question,
                cache_path=cache_path
            )

            st.session_state.vector_ready = True

        # ----------------------------------
        # Display output
        # ----------------------------------
        st.subheader("Answer")
        st.write(answer)

        with st.expander("Retrieved Context"):
            st.write(context)

        with st.expander("Evaluation"):
            st.json(evaluation)
