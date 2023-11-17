# NolwaziGPT Chatbot RAG

NzululwaziGPT is an API that provides human-like text responses to any question you might have on organizational documents.

This README will guide you through the process of setting up and testing the API locally.

## Requirements

- Python >= 3.9
- Virtualenv (optional, but recommended)
- Other dependencies as listed in `requirements.txt`

## Local Installation

1. **Clone the Repository**: 

   ```bash
   git clone https://github.com/Thembisile/nzulu_api.git
   cd nzulu_webapp
   ```

2. **Create a Virtual Environment** (optional):

   ```bash
   python3 -m venv myenv
   myenv\Scripts\activate.bat  # On Linux, use `source myenv/bin/activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Downloading a Model**:

   You may use the below link to download the model: 

> [llama-2-13b-chat.ggmlv3.q4_1.bin](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_1.bin)

>- Create a folder called `models` and save the model in that folder
>- Update the `.env` file to the relative path of your model and ensure the correct model is linked on your `.env`.

5. **Configure Environment Variables** (if applicable):

   Modify `.env` file with your specific configuration, or export variables manually.

6. **Run the Server**:

   ```bash
   python manage.py runserver
   ```

The API should now be running at `http://127.0.0.1:8000/`.

## Testing the API endpoints using Django REST Framework

To access the Upload API, use the following endpoint : 
 `http://127.0.0.1:8000/api/upload`

- You will be prompted to insert a file(type:pdf,word,txt and csv📁) and add that file into a collection(category).
- Enter the collection name

To access the Chat API, use the following endpoint : 
 `http://127.0.0.1:8000/api/chat`
- You will be prompted to enter your query(type:string=>"Enter your prompt"), which should be any question you'd like to ask based any documents uploaded as long as the correct collection has been selected.
- Insert the collection name from which you would like to query.

  
## Testing the API using cURL

You can test the API using tools like `curl`, Django Rest Frame, or any HTTP client library in a programming language of your choice.

Here's an example of how to call an endpoint using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d '{"query":"your_query", "collection_name":"your_collection"}'
```

> `"your_query"` = The input query or question to the model
> `"your_collection"` = The collection or category in which the document you want to question resides e.g Policies, Employee Relations etc

Replace `"your_query"` and `"your_collection"` with the appropriate values for your API call.

## Documentation
## **Nzulu API Documentation**

### **1. Upload Documents Endpoint**

**Endpoint**: `/api/upload`

**Method**: POST

**Description**: This endpoint allows users to upload documents that will be embedded and stored for retrieval.

**Headers**:
- Content-Type: `multipart/form-data`

**Body**:
- `file`: The document you wish to upload (type: file).
- `collection_name`: The name of the collection to which this document should belong (type: string).

**Sample cURL**:
```bash
curl --location --request POST 'http://localhost:8000/api/upload' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@path_to_your_file.txt' \
--form 'collection_name=sample_collection'
```

### **2. Chat Endpoint**

**Endpoint**: `/api/chat`

**Method**: POST

**Description**: Send a query to retrieve answers based on the uploaded documents.

**Headers**:
- Content-Type: `application/json`

**Body**:
- `query`: The question or statement you wish to get an answer for (type: string).
- `collection_name`: The name of the collection you're querying against (type: string).

**Sample cURL**:
```bash
curl --location --request POST 'http://localhost:8000/api/chat' \
--header 'Content-Type: application/json' \
--data-raw '{
    "query": "Ask your question here",
    "collection_name": "sample_collection"
}'
```

## Contact

If you have any questions or feedback, please feel free to [contact me](mailto:shaundamon09@gmail.com).

---
