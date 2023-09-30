from langchain.document_loaders import JSONLoader  # importar clase
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils import get_file_path


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


def main():
    documents = load_documents(get_file_path())
    print(len(documents))
    print(documents[0])


if __name__ == "__main__":
    main()
