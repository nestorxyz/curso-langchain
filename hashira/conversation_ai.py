from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils import get_file_path


# metadata: title, repo_owner, repo_name
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["title"] = record.get("title")
    metadata["repo_owner"] = record.get("repo_owner")
    metadata["repo_name"] = record.get("repo_name")

    return metadata


def load_documents(path):
    loader = JSONLoader(
        path,
        json_lines=True,
        jq_schema=".",
        content_key="text",
        metadata_func=metadata_func,
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
