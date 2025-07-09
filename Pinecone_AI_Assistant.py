from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import dotenv
import os 
from dotenv import load_dotenv

pc_clevel = Pinecone(api_key="<Your api key>")
pc_finance = Pinecone(api_key="<Your api key>")
assistant_clevel = pc_clevel.assistant.Assistant(assistant_name="<Your assistant name>")


assistant_finance = pc_finance.assistant.Assistant(
    assistant_name="<Your assistant name>", 
)
###upload data into your pincone datasbe for the AI assistant (Finance assistant)
### ONLY ONCE
# response_finance = assistant_finance.upload_file(
#     file_path="financial_summary.md",
#     timeout=None
# )
###upload data into your pincone datasbe for the Ai assistant (C-Level assistant)
####### ONLY ONCE
# for i in [path to your files]:
#     response_clevel = assistant_finance.upload_file(
#         file_path=i,
#         timeout=None
    # )
def clevel_response(query):
    """Generate a response using the Pinecone Assistant."""
    print("Pinecone Assistant: Processing query...")
     # Add the user message
    msg = Message(content=f"""Please answer the query in detail.
        Query: {query}""")
    resp = assistant_clevel.chat(messages=[msg])
    return resp["message"]["content"]


def finance_response(query):
    """Generate a response using the Pinecone Assistant."""
    print("Pinecone Assistant: Processing query...")
     # Add the user message
    msg = Message(content=f"""Please answer the query in detail.
        Query: {query}""")
    resp = assistant_finance.chat(messages=[msg])
    return resp["message"]["content"]
















