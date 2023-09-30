# model imports
from langchain.document_loaders import JSONLoader  # importar clase
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# external imports
from rich.console import Console

# local imports
from utils import get_file_path

console = Console()
recreate_chroma_db = False


# funcion metadata para retornar title, repo_owner, repo_name en la metadata del documento
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["title"] = record.get("title")
    metadata["repo_owner"] = record.get("repo_owner")
    metadata["repo_name"] = record.get("repo_name")

    return metadata


def load_documents(path):
    loader = JSONLoader(
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


def get_chroma_db(embeddings, documents, path):
    if recreate_chroma_db:
        console.print("Creating Chroma DB")
        return Chroma.from_documents(
            documents=documents, embedding=embeddings, persist_directory=path
        )
    else:
        console.print("Loading Chroma DB")
        return Chroma(persist_directory=path, embedding_function=embeddings)


def main():
    documents = load_documents(get_file_path())
    embeddings = HuggingFaceEmbeddings()

    vectorstore_chroma = get_chroma_db(embeddings, documents, "chroma_docs")
    console.print(f"[green]Documents {len(documents)} loaded[/green]")


if __name__ == "__main__":
    main()
