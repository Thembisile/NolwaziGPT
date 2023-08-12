from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import os
import urllib
from tqdm import tqdm
import ingest
import time
from django.http import JsonResponse 

from .serializers import UploadSerializer, ChatSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from db_config import client
from .models import Documents


def model_download():
    model_type = os.environ.get('MODEL_TYPE')
    url = None
    if model_type == "LlamaCpp":
        url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_1.bin"
    elif model_type == "GPT4All":
        url = "https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin"
    if url is not None:
        folder = "models"
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.join(folder, os.path.basename(parsed_url.path))
        # Check if the file already exists
        if not os.path.exists(filename):
            print("Model download started.")
            # Create the folder if it doesn't exist
            os.makedirs(folder, exist_ok=True)
            # Use requests to download the file
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024  
                t = tqdm(total=total_size, unit='iB', unit_scale=True)
                with open(filename, 'wb') as f:
                    for data in response.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()
                if total_size != 0 and t.n != total_size:
                    print("ERROR, something went wrong while downloading the model.")
                print("Model downloaded.")
                global model_path
                model_path = filename
                os.environ['MODEL_PATH'] = filename


def embed_documents(files, collection_name):
    print("Embedding documents...")
    # Save the files in the source_documents directory
    saved_files = []
    for file in files:
        file_path = os.path.join('source_documents', file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        saved_files.append(file_path)
    # Now that the files are saved, call ingest.py script
    try:
        ingest.main(collection_name)
        print("Documents embedded successfully.")
    except Exception as e:
        print(f"Error loading documents: {str(e)}")
    return saved_files

def process_query(query, collection_name):
    print(f"Model path: {os.environ.get('MODEL_PATH')}")

    embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
    print(f"Embeddings model name: {embeddings_model_name}")
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    # Use the ChromaDB client to create a Chroma instance
    db = Chroma(client=client, embedding_function=embeddings,
                collection_name=collection_name)
    retriever = db.as_retriever()

    # Prepare the LLM
    callbacks = [StreamingStdOutCallbackHandler()]
    model_type = os.environ.get('MODEL_TYPE')
    model_path = os.environ.get('MODEL_PATH')
    model_n_ctx = int(os.environ.get('MODEL_N_CTX'))

    if model_type == "LlamaCpp":
        print("Using LlamaCpp model...")
        llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, # input={"temperature": 0.75, "max_length": 2000, "top_p": 1},
                       callbacks=callbacks, verbose=False)
    elif model_type == "GPT4All":
        print("Using GPT4All model...")
        llm = GPT4All(model=model_path, backend='gptj',
                      callbacks=callbacks, verbose=False)
    else:
        raise ValueError(f"Model {model_type} not supported!")
   
    # store model response start time in a var
    start_time = time.time()
    
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False)

    # Get the answer from the chain
    res = qa(query)
    print("Query processed.")
    print(res)
    answer = res['result']

    # Time it took for the model to provide response
    end_time = time.time() 
    total_time = end_time - start_time  
    print(f"Response generation completed in: {round(total_time, 2)} seconds.")
    return answer


class UploadView(APIView):
    serializer_class = UploadSerializer

    def post(self, request):
        print("Embedding request received.")
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data.get('file')
            collection_name = serializer.validated_data.get('collection_name')
            
            # We put the file into a list to use it with the embed_documents function
            saved_files = embed_documents([file], collection_name)
            print("Embedding request completed.")

            return Response({"message": "File embedded successfully", "saved_files": saved_files})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatView(APIView):
    serializer_class = ChatSerializer

    def post(self, request):
        print("Nzulu's response request received..")
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            query = serializer.validated_data.get('query')
            collection_name = serializer.validated_data.get('collection_name')

            print("Nzulu is processing the query...")
            answers = process_query(query, collection_name)
            print("Nzulu has processed the query.")

            return Response({"answers": answers})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

