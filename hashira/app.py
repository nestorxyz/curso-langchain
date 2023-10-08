import openai
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain, RetrievalQA

from utils import get_file_path
from rich.console import Console

console = Console()


def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["title"] = record.get("title")
    metadata["repo_owner"] = record.get("repo_owner")
    metadata["repo_name"] = record.get("repo_name")

    return metadata


def load_documents(path):
    loader = JSONLoader(  # JSONLoader es una clase que se encarga de cargar documentos desde un archivo jsonl
        path,
        json_lines=True,  # indica que el archivo es un jsonl
        jq_schema=".",  # indica que el jsonl tiene un solo elemento por linea, más info en https://python.langchain.com/docs/modules/data_connection/document_loaders/json#common-json-structures-with-jq-schema
        content_key="text",  # indica que el contenido del documento está en la llave "text"
        metadata_func=metadata_func,  # indica que la función metadata_func se usará para obtener la metadata del documento
    )
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600, length_function=len, chunk_overlap=160
    )

    return text_splitter.split_documents(data)


def get_chroma_db(embeddings, documents, path, recreate_chroma_db=False):
    if recreate_chroma_db:
        console.print("Creating Chroma DB")
        return Chroma.from_documents(
            documents=documents, embedding=embeddings, persist_directory=path
        )
    else:
        console.print("Loading Chroma DB")
        return Chroma(persist_directory=path, embedding_function=embeddings)


def process_qa_query(query: str, llm: ChatOpenAI, retriever: any):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    return qa_chain.run(query)


def process_memory_query(
    query: str, llm: ChatOpenAI, retriever: any, chat_history: any
):
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    print(f"the chat history is {chat_history}")
    result = conversation({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    return result["answer"]


if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vectorstore_chroma" not in st.session_state:
    embeddings = HuggingFaceEmbeddings()
    documents = load_documents(get_file_path())

    st.session_state.vectorstore_chroma = get_chroma_db(
        embeddings, documents, "chroma_docs", recreate_chroma_db=False
    )
    console.print("Chroma DB loaded")

st.title("Chat with HugginFace Docs 🤗")

with st.sidebar:
    st.markdown(
        """
        # Chat with HugginFace Docs 🤗
        This is an example of a chatbot that uses a vectorstore to retrieve documents and a language model to generate answers based on the retrieved documents.
        A Chroma DB is used to retrieve the most relevant documents to the question.
        """
    )
    openai_api_key = st.text_input("OpenAI API Key")
    openai.api_key = openai_api_key

    option = st.selectbox(
        "What kind of chat do you want?", ("Question Answering", "Memory")
    )


with st.chat_message("assistant"):
    st.markdown(
        "hi!! what do you want to ask me about transformers and artificial intelligence?"
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
            st.stop()

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2,
            max_tokens=200,
            openai_api_key=openai_api_key,
        )
        retriever = st.session_state.vectorstore_chroma.as_retriever(
            search_kwargs={"k": 3}
        )
        chat_history = st.session_state.chat_history
        message_placeholder.markdown("Thinking...")

        if option == "Question Answering":
            console.print("Question Answering")
            response = process_qa_query(prompt, llm, retriever)
        elif option == "Memory":
            console.print("Memory")
            response = process_memory_query(prompt, llm, retriever, chat_history)

        message_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
