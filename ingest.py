import os
import sys
import glob
from typing import List
from dotenv import load_dotenv
import argparse
from multiprocessing import Pool
from tqdm import tqdm
from langchain.vectorstores import Chroma

from langchain.document_loaders import (
    CSVLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredWordDocumentLoader,
    Docx2txtLoader
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from db_config import CHROMA_SETTINGS


load_dotenv()
db = None

LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".docx": (Docx2txtLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}


def load_single_document(file_path: str) -> Document:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()[0]

    raise ValueError(f"Unsupported file extension '{ext}'")


def load_documents(source_dir: str) -> List[Document]:
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(all_files), desc='Loading documents', ncols=80) as pbar:
            for i, doc in enumerate(pool.imap_unordered(load_single_document, all_files)):
                results.append(doc)
                pbar.update()

    return results


def does_vectorstore_exist(persist_directory: str) -> bool:
    if os.path.exists(os.path.join(persist_directory, 'index')):
        if os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(persist_directory, 'chroma-embeddings.parquet')):
            list_index_files = glob.glob(os.path.join(persist_directory, 'index/*.bin'))
            list_index_files += glob.glob(os.path.join(persist_directory, 'index/*.pkl'))
            if len(list_index_files) > 3:
                return True
    return False


def main(collection):
    global db
    persist_directory = os.environ.get('PERSIST_DIRECTORY')
    source_directory = os.environ.get('SOURCE_DIRECTORY', 'source_documents')
    embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME')
    os.makedirs(source_directory, exist_ok=True)

    print(f"Loading documents from {source_directory}")
    chunk_size = 500
    chunk_overlap = 50
    documents = load_documents(source_directory)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Loaded {len(documents)} documents from {source_directory}")
    print(f"Split into {len(texts) if texts else 0} chunks of text (max. {chunk_size} characters each)")

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    if does_vectorstore_exist(persist_directory):
        print(f"Appending to existing vectorstore at {persist_directory}")
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
        db.add_documents(texts)
    else:
        print("Creating new vectorstore")
        db = Chroma.from_documents(texts, embeddings, collection_name=collection, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS)

    db.persist()

    # # Visualize Embeddings in 3D
    # from chromaviz import visualize_collection
    # visualize_collection(db._collection)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--collection", help="Saves the embedding in a collection name as specified")
        args = parser.parse_args()
        main(args.collection)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
