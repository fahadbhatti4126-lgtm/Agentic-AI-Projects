import streamlit as st
from dotenv import load_dotenv

from document_processor import (
    extract_text_from_pdf,
    create_vector_database,
    retrieve_relevant_text
)

from langchain_groq import ChatGroq
from models import DocumentAnalysis

load_dotenv()


# ==========================================
# AI MODEL
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ==========================================
# DOCUMENT ANALYSIS
# ==========================================

def analyze_document(vector_db):

    query = """
    What are the main facts, purpose, important information,
    and key points contained in this document?
    """

    relevant_text = retrieve_relevant_text(
        vector_db,
        query
    )

    prompt = f"""
You are an intelligent document analysis agent.

Analyze the document using ONLY the retrieved information below.

Retrieved Information:
{relevant_text}

Return ONLY valid JSON.

The JSON must have exactly these four fields:

{{
    "title": "document title",
    "summary": "short summary of the document",
    "key_points": [
        "important point 1",
        "important point 2",
        "important point 3"
    ],
    "document_type": "type of document"
}}

Do not add markdown.
Do not add explanations outside the JSON.
Do not invent information.
"""

    response = llm.invoke(prompt)

    result = DocumentAnalysis.model_validate_json(
        response.content
    )

    return result


# ==========================================
# QUESTION ANSWERING
# ==========================================

def answer_question(vector_db, question):

    # Retrieve relevant information
    relevant_text = retrieve_relevant_text(
        vector_db,
        question
    )

    prompt = f"""
You are a document question-answering agent.

Answer the user's question using ONLY the retrieved
information from the document.

Retrieved Information:
{relevant_text}

User Question:
{question}

Rules:

- Answer clearly and directly.
- Use only information from the document.
- Do not invent information.
- If the answer is not available in the retrieved
  information, say:
  "The answer was not found in the document."
"""

    response = llm.invoke(prompt)

    return response.content


# ==========================================
# STREAMLIT PAGE
# ==========================================

st.set_page_config(
    page_title="AI Document Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("📄 AI Document Analyzer")

st.write(
    "Upload a PDF, analyze it, and ask questions "
    "about its content."
)


# ==========================================
# PDF UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)


if uploaded_file:

    st.success("PDF uploaded successfully!")


    # ======================================
    # EXTRACT TEXT + CREATE VECTOR DATABASE
    # ======================================

    if "vector_db" not in st.session_state:

        with st.spinner(
            "Processing document..."
        ):

            try:

                text = extract_text_from_pdf(
                    uploaded_file
                )

                if not text.strip():

                    st.error(
                        "No readable text was found "
                        "in this PDF."
                    )

                    st.stop()


                vector_db = create_vector_database(
                    text
                )

                st.session_state.vector_db = vector_db

                st.success(
                    "Document processed successfully!"
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )

                st.stop()


    vector_db = st.session_state.vector_db


    # ======================================
    # DOCUMENT ANALYSIS
    # ======================================

    st.subheader(
        "📋 Document Analysis"
    )

    if st.button(
        "🔍 Analyze Document"
    ):

        with st.spinner(
            "Analyzing document..."
        ):

            try:

                result = analyze_document(
                    vector_db
                )

                st.success(
                    "Analysis completed!"
                )


                st.write(
                    f"**Title:** {result.title}"
                )

                st.write(
                    f"**Document Type:** "
                    f"{result.document_type}"
                )


                st.subheader(
                    "📝 Summary"
                )

                st.write(
                    result.summary
                )


                st.subheader(
                    "🔑 Key Points"
                )

                for point in result.key_points:

                    st.write(
                        f"• {point}"
                    )


            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )


    # ======================================
    # ASK QUESTIONS
    # ======================================

    st.divider()

    st.subheader(
        "💬 Ask Questions About Your PDF"
    )

    question = st.text_input(
        "Enter your question:",
        placeholder="Example: What is the admission process?"
    )


    if st.button(
        "🤖 Ask AI"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "Searching the document..."
            ):

                try:

                    answer = answer_question(
                        vector_db,
                        question
                    )

                    st.subheader(
                        "💡 Answer"
                    )

                    st.write(
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"An error occurred: {str(e)}"
                    )