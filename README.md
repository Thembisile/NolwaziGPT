# NzululwaziGPT API

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

4. **Configure Environment Variables** (if applicable):

   Modify `.env` file with your specific configuration, or export variables manually.

5. **Run the Server**:

   ```bash
   python manage.py runserver
   ```

The API should now be running at `http://127.0.0.1:8000/`.

## Testing the API

You can test the API using tools like `curl`, Django Rest Frame, or any HTTP client library in a programming language of your choice.

Here's an example of how to call an endpoint using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d '{"query":"your_query", "collection_name":"your_collection"}'
```

> `"your_query"` = The input query or question to the model
> `"your_collection"` = The collection or category in which the document you want to question resides e.g Policies, Employee Relations etc

Replace `"your_query"` and `"your_collection"` with the appropriate values for your API call.

## Documentation

To be included once API in production [API Documentation](#).


## Contact

If you have any questions or feedback, please feel free to [contact me](mailto:shaundamon09@gmail.com).

---
