from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Load private knowledge base
loader = TextLoader(
    "knowledge.txt",
    encoding="utf-8"
)

documents = loader.load()


# Split knowledge into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)


# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create Chroma vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db",
    collection_name="student_knowledge"
)


# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


def retrieve_information(question):
    """Retrieve relevant information from the private knowledge base."""

    documents = retriever.invoke(question)

    return documents