import io
import os
from dotenv import load_dotenv
import google.generativeai as genai
def genai_response(context, query):
    """
    Generate a response using Google Gemini AI based on the provided context and query.
    """
    print(f"Gemini LLM: Processing query with {len(context)} characters of context")
    
    # Configure the API key
    genai.configure(api_key="<Your api key>")
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
