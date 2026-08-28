import streamlit as st

from workflow import run_workflow


# Page settings
st.set_page_config(
    page_title="University Knowledge Agent",
    page_icon="🎓",
    layout="centered"
)


# Custom CSS
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #07111f 0%,
            #102a43 50%,
            #123b5d 100%
        );
        color: white;
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: white;
    }

    .subtitle {
        text-align: center;
        color: #7dd3fc;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .info-card {
        background: linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.85),
            rgba(6, 182, 212, 0.8)
        );
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
    }

    .info-card p {
        color: #e0f2fe;
    }

    label {
        color: white !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(125, 211, 252, 0.5);
        border-radius: 12px;
    }

    div[data-baseweb="input"] input {
        color: white !important;
    }

    .stButton > button {
        width: 100%;
        height: 50px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(
            90deg,
            #2563eb,
            #06b6d4
        );
        color: white;
        font-size: 17px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Header
st.markdown(
    '<div class="title">🎓 Knowledge-Based Decision Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">University of Layyah • Agentic AI Project 2</div>',
    unsafe_allow_html=True
)


# Information card
st.markdown(
    """
    <div class="info-card">
        <h2>📚 Private Knowledge Assistant</h2>
        <p>
            Ask questions about the information stored in the
            private course knowledge base.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# Question input
question = st.text_input(
    "💬 Ask your question",
    placeholder="Example: What are the main concepts of Project 2?"
)


# Ask button
if st.button("🔍 Ask Knowledge Agent"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 Searching the private knowledge base..."):

            try:

                answer = run_workflow(question)

                st.subheader("🤖 Agent Answer")

                st.success(answer)

            except Exception as e:

                st.error(f"Error: {e}")