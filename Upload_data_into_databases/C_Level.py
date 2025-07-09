from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import dotenv
import os 
from dotenv import load_dotenv

pc_clevel = Pinecone(api_key="< YOUR_API_KEY >")
pc_finance = Pinecone(api_key="< YOUR_API_KEY > ")
assistant_clevel = pc_clevel.assistant.Assistant(assistant_name="rag-assistant-clevel")

assistant_finance = pc_finance.assistant.Assistant(
    assistant_name="rag-assistant-finance", 
)
#Upload Finance data 
# upload  the data only once 
response_finance = assistant_finance.upload_file(
    file_path="<Path to financial_summary.md> ",
    timeout=None
)
#Upload merged  data and HR data for the C_Level role
# upload  the data only once 
for i in ["< Path to C_Level_Merged_codebasics.pdf>","<Path to HR_Final_JSON.json> "]:
    response_clevel = assistant_finance.upload_file(
        file_path=i,
        timeout=None
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





# res_c=clevel_response("what happened in Q2 april to june 2024 financial report")
# res_f=finance_response("what happened in Q2 april to june 2024 financial report")

# print(res_c)
# print('--------------------------------------------------------------------------')
# print(res_f)












