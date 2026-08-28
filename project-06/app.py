import streamlit as st

from workflow import run_workflow


st.set_page_config(
    page_title="University of Layyah - Telecom Agent",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 Telecom Agentic AI Assistant")

st.write(
    "LangGraph + Agent + Tools based Telecom Customer Support Assistant"
)


user_message = st.text_input(
    "💬 Enter your message",
    placeholder="Example: My mobile internet is very slow."
)


if st.button("🚀 Ask Agent"):

    if not user_message.strip():

        st.warning("Please enter a message.")

    else:

        with st.spinner("🤖 Agent is thinking..."):

            try:

                response = run_workflow(user_message)

                st.subheader("🤖 Agent Response")

                st.success(response)

            except Exception as e:

                st.error(f"Error: {e}")