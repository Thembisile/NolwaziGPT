import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import time
import requests

API_URL = 'http://127.0.0.1:8000'

def process_query(query, collection):
    url = f"{API_URL}/api/chat"
    response = requests.post(url, json={"query": query, "collection_name": collection})
    return response.json().get('answers', '')

def main():
    st.markdown("<h1 style='text-align: center; color: black;'>💬 NzuluwaziGPT</h1>", unsafe_allow_html=True)

    # Document embedding
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("Choose a file to embed", type=["txt", "pdf"], accept_multiple_files=False)
    collection_name = st.text_input("Collection Name:")
    if st.button("Upload") and uploaded_file:
        embed_documents(uploaded_file, collection_name)

    colored_header(label='', description='', color_name='blue-30')

    st.header("ChatUI")
    # Assistant Response
    if 'generated' not in st.session_state:
        st.session_state['generated'] = [
            "Hi, My name is Nzululwazi but you may call me Nzulu, How may I help you?"]

    # user question
    if 'user' not in st.session_state:
        st.session_state['user'] = ['Hi!']

    response_container = st.container()
    input_container = st.container()

    # get user input
    def get_text():
        if 'input_text' not in st.session_state:
            st.session_state['input_text'] = ""
        input_text = st.text_input(
            "You: ", st.session_state['input_text'], key="input")
        return input_text

    # Clear input text
    st.session_state['input_text'] = ''

    # Applying the user input box
    with input_container:
        user_input = get_text()
        submit_button = st.button('Submit')

        # If the user has input a query, ask for the collection name
        # user_input = st.text_input("You:", key="user_input")
        query_collection_name = st.text_input("Category", key="query_collection_name")
        if user_input and submit_button:
            if not query_collection_name:  # Check if the query_collection_name is empty
                st.error("Error: Category cannot be empty!",  icon="🚨")
            else:    
                try:
                    res = process_query(user_input, query_collection_name)
                    answer = res

                    st.session_state.user.append(user_input)
                    st.session_state.generated.append(answer)

                except Exception as e:
                    st.write(f"An error occurred: {e}")

    with response_container:
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['user'][i], is_user=True, key=str(
                    i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i],
                        key=str(i), avatar_style="avataaars")

def embed_documents(uploaded_file, collection_name):
    url = f"{API_URL}/api/upload"
    files_to_send = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
    response = requests.post(url, files=files_to_send, data={'collection_name': collection_name})
    result = response.json()

    if response.status_code == 200:
        st.success(result['message'])
        st.write("Saved Files:", result['saved_files'])
    else:
        st.error(f"Error: {result}")

    return result

if __name__ == "__main__":
    main()
