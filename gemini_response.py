# import os, google.genai
# from opik.integrations.genai import track_genai
# import fitz  # PyMuPDF


import io
import os
from dotenv import load_dotenv

import google.generativeai as genai
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.documents import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain_cohere import ChatCohere, CohereEmbeddings
# api_key='AIzaSyDY9wjuzr7N4TXDF6f93JUzDOId6iZhha0'
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")
# # load_dotenv()
# os.environ["OPIK_API_KEY"] = "4YxvviQqzPgUKXqKHXVaQyLDV" 
# os.environ["OPIK_WORKSPACE"] = "rohith8074"

# client = google.genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY", "default_key"))
# gemini_client = track_genai(client)
# response = gemini_client.models.generate_content(
#     model="gemini-2.0-flash-001", contents="Write a haiku about AI engineering."
# )
# print(response.text)
# def genai_response(context,query):
#     response = model.generate_content(["""You are an helpful assistant. 
#     You will be given a conetxt and based upon that asnwer the users qiery in detail.
#     query: {query}
#     context: {context}  """])









import google.generativeai as genai
def genai_response(context, query):
    """
    Generate a response using Google Gemini AI based on the provided context and query.
    """
    # if not context or not context.strip():
    #     return "⚠️ **No Context Available**: Unable to find relevant information in the knowledge base for your query."
    
    # if not query or not query.strip():
    #     return "⚠️ **Invalid Query**: Please provide a valid question."
    import google.generativeai as genai

def genai_response(context, query):
    """
    Generate a response using Google Gemini AI based on the provided context and query.
    """
    print(f"Gemini LLM: Processing query with {len(context)} characters of context")
    
    # Configure the API key
    genai.configure(api_key="AIzaSyC1z8a_bV7pOkszr0lMQDSnyQfJfwapXLw")
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    
    response = model.generate_content(
        f"""
        You are a helpful assistant. 
        You will be given a context and based upon that answer the user's query in detail.
        query: {query}
        context: {context}
        """
    )
    return response.text
