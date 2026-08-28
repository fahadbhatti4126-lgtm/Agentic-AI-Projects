import streamlit as st

from communication_agent import create_communication


# Page settings
st.set_page_config(
    page_title="University of Layyah - Communication AI",
    page_icon="📧",
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
        padding-bottom: 2rem;
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
        font-size: 16px;
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

    div[data-baseweb="input"] input::placeholder {
        color: #b6c7d9 !important;
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
        box-shadow: 0 5px 18px rgba(6, 182, 212, 0.35);
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #06b6d4,
            #2563eb
        );
        transform: translateY(-2px);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Header
st.markdown(
    '<div class="title">📧 Intelligent Communication Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">University of Layyah • Agentic AI Project 5</div>',
    unsafe_allow_html=True
)


# Information card
st.markdown(
    """
    <div class="info-card">
        <h2>📨 Smart Communication AI</h2>
        <p>
            The AI analyzes your request and prepares
            an appropriate email or notification.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# User request
request = st.text_input(
    "💬 Enter your communication request",
    placeholder="Example: Prepare an email to Ali about tomorrow's meeting."
)


# Button
if st.button("🚀 Create Communication"):

    if not request.strip():

        st.warning("Please enter a request.")

    else:

        with st.spinner("🤖 Analyzing request and selecting the right tool..."):

            try:

                result = create_communication(request)

                st.subheader("📨 Result")

                st.success(result)

            except Exception as e:

                st.error(f"Error: {e}")