'''import os
import streamlit as st

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

## Uncomment the following files since I am not using pipenv as your virtual environment manager
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


DB_FAISS_PATH="vectorstore/db_faiss"
@st.cache_resource
def get_vectorstore():
    embedding_model=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db=FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

def load_llm(huggingface_repo_id, HF_TOKEN):
    llm=HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        task="text-generation",
        temperature=0.5,
        model_kwargs={"token":HF_TOKEN,
                      "max_length":"512"}
    )
    return llm


def main():
    st.title("Ask Chatbot!")

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt=st.chat_input("Pass your prompt here")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role':'user', 'content': prompt})
        
        CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""
        HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
        HF_TOKEN=os.environ.get("HF_TOKEN")
        
        try: 
            vectorstore=get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load the vector store")

            qa_chain=RetrievalQA.from_chain_type(
                llm=load_llm(huggingface_repo_id=HUGGINGFACE_REPO_ID, HF_TOKEN=HF_TOKEN),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={'k':3}),
                return_source_documents=True,
                chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
            )

            response=qa_chain.invoke({'query':prompt})

            result=response["result"]
            source_documents=response["source_documents"]
            
            st.chat_message('assistant').markdown(result)

            with st.expander("🔍 Show Sources"):
                for i, doc in enumerate(source_documents, 1):
                    metadata = doc.metadata
                    source_info = f"**Source {i}:**\n- File: `{metadata.get('source', 'N/A')}`\n- Page: {metadata.get('page_label', metadata.get('page', 'N/A'))}\n"
                    page_excerpt = doc.page_content.strip()[:500] + ("..." if len(doc.page_content) > 500 else "")
                    st.markdown(source_info)
                    st.code(page_excerpt)

# Save only the main response in chat history (not the source docs)
            st.session_state.messages.append({'role':'assistant', 'content': result})

        except Exception as e:
            st.error(f"Error: {str(e)}") 
        
       
        

        

if __name__ == "__main__":
    main()'''
    

import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv(find_dotenv())

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def set_custom_prompt(context, question):
    return f"""
You are a helpful and knowledgeable medical assistant.

Based on the context below, write a clear, friendly, and conversational answer to the user's question.
Use full sentences and paragraph form. Do not use bullet points, numbered steps, or lists of any kind — even if the question asks for them.
Avoid restating the question. Only use the information in the context provided.

Context:
{context}

Question:
{question}

Answer:
"""


def load_inference_client():
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("🤖 HF_TOKEN is missing in environment variables.")
    
    return InferenceClient(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        token=hf_token
    )

def main():
    st.title("🩺 Medibot: Ask Your AI Medical Assistant!")

    # Initialize session state for storing chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    # Get the user input
    user_input = st.chat_input("Type your medical question here...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # Retrieve the vectorstore
            vectorstore = get_vectorstore()
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

            # 👋 Simple greeting detection
            greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
            if user_input.strip().lower() in greetings:
                answer = "👋 Hello! I'm your medical assistant. How can I help you today?"
                st.chat_message("assistant").markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                # Concatenate all previous messages as context
                combined_context = "\n\n".join([message["content"] for message in st.session_state.messages])
                prompt = set_custom_prompt(combined_context, user_input)

                # Query the model
                client = load_inference_client()
                response = client.text_generation(
                    prompt=prompt,
                    max_new_tokens=512,
                    temperature=0.5
                )
                answer = response.strip()
                st.chat_message("assistant").markdown(answer)

                # Show sources if available
                with st.expander("🔍 Show Sources"):
                    docs = retriever.get_relevant_documents(user_input)
                    for i, doc in enumerate(docs, 1):
                        metadata = doc.metadata
                        source_info = f"**Source {i}:**\n- File: `{metadata.get('source', 'N/A')}`\n- Page: {metadata.get('page_label', metadata.get('page', 'N/A'))}"
                        excerpt = doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else "")
                        st.markdown(source_info)
                        st.code(excerpt)

                # Append the response to session history
                st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
