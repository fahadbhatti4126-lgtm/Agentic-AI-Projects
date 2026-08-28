import streamlit as st

from workflow import solve_problem


# Page settings
st.set_page_config(
    page_title="University of Layyah - Multi-Agent AI",
    page_icon="🤖",
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
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    .info-card p {
        color: #e0f2fe;
        font-size: 16px;
    }

    label {
        color: white !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="textarea"] {
        background-color: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(125, 211, 252, 0.5);
        border-radius: 12px;
    }

    div[data-baseweb="textarea"] textarea {
        color: white !important;
    }

    div[data-baseweb="textarea"] textarea::placeholder {
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
    '<div class="title">🤖 Multi-Agent Problem Solving System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">University of Layyah • Agentic AI Project 3</div>',
    unsafe_allow_html=True
)


# Information card
st.markdown(
    """
    <div class="info-card">
        <h2>🧠 Multi-Agent AI</h2>
        <p>
            Research Agent → Analysis Agent → Reviewer Agent
        </p>
        <p>
            Multiple specialized agents collaborate to solve your problem.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# User problem
problem = st.text_input(
    "💬 Enter your problem",
    placeholder="Example: I want to learn Python but don't know where to start."

)


# Execute button
if st.button("🚀 Solve Problem"):

    if not problem.strip():

        st.warning("Please enter a problem.")

    else:

        with st.spinner(
            "🤖 Research Agent → Analysis Agent → Reviewer Agent..."
        ):

            try:

                answer = solve_problem(problem)

                st.subheader("🤖 Final Answer")

                st.success(answer)

            except Exception as e:

                st.error(f"Error: {e}")