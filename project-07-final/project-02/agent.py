import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from rag import retrieve_information


load_dotenv()


# Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_agent(question):
    """
    Retrieve information from the private knowledge base
    and use the retrieved context to answer the question.
    """

    documents = retrieve_information(question)

    if not documents:
        return "I could not find relevant information in the knowledge base."

    context = "\n\n---\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a Knowledge-Based Decision Agent.

Answer the user's question using ONLY the information
provided in the private knowledge base below.

Do not invent information.

If the answer cannot be found in the knowledge base,
say:

"I could not find relevant information in the knowledge base."

Private Knowledge Base:
{context}

User Question:
{question}

Provide a clear and concise answer.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content