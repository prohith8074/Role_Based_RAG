from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import dotenv
import os 
from dotenv import load_dotenv

pc_clevel = Pinecone(api_key="pcsk_73Vvcj_Gz7JMeo3JYaCx13XLgshufDATyoUNxBChvTZNp2GXQb9hVevzRUiksH6HQ1TqVp")
pc_finance = Pinecone(api_key="pcsk_3YypN6_JxsD2AGkEYjwHEVE12P3bBwHMAxCjdJpqia2rfBg84h9QbHnnM1rnAHdvqe5MU2")
assistant_clevel = pc_clevel.assistant.Assistant(assistant_name="rag-assistant-clevel")
# assistant_finance = pc_clevel.assistant.Assistant(assistant_name="rag-assistant-finance")
# from pinecone import Pinecone
# pc = Pinecone(api_key="YOUR_API_KEY")

assistant_finance = pc_finance.assistant.Assistant(
    assistant_name="rag-assistant-finance", 
)

# response_finance = assistant_finance.upload_file(
#     file_path="financial_summary.md",
#     timeout=None
# )
# for i in ["Merged_codebasics.pdf","HR_Final_JSON.json"]:
#     response_clevel = assistant_finance.upload_file(
#         file_path=i,
#         timeout=None
    # )
def clevel_response(query):
    """Generate a response using the Pinecone Assistant."""
    # if not context or not context.strip():
    #     return "⚠️ **No Context Available**: Unable to find relevant information in the knowledge base for your query."
    
    # if not user_query or not user_query.strip():
    #     return "⚠️ **Invalid Query**: Please provide a valid question."
    
    print("Pinecone Assistant: Processing query...")
     # Add the user message
    msg = Message(content=f"""Please answer the query in detail.
        Query: {query}""")
    resp = assistant_clevel.chat(messages=[msg])
    return resp["message"]["content"]
# ans=response("explain Q1 jan to march financial report in detail")
# print(ans)

def finance_response(query):
    """Generate a response using the Pinecone Assistant."""
    # if not context or not context.strip():
    #     return "⚠️ **No Context Available**: Unable to find relevant information in the knowledge base for your query."
    
    # if not user_query or not user_query.strip():
    #     return "⚠️ **Invalid Query**: Please provide a valid question."
    
    print("Pinecone Assistant: Processing query...")
     # Add the user message
    msg = Message(content=f"""Please answer the query in detail.
        Query: {query}""")
    resp = assistant_finance.chat(messages=[msg])
    return resp["message"]["content"]
# ans=response("explain Q1 jan to march financial report in detail")
# print(ans)




# res_c=clevel_response("what happened in Q2 april to june 2024 financial report")
# res_f=finance_response("what happened in Q2 april to june 2024 financial report")

# print(res_c)
# print('--------------------------------------------------------------------------')
# print(res_f)













# from pinecone import Pinecone
# pc = Pinecone(api_key="YOUR_API_KEY")

# assistant = pc.assistant.Assistant(
#     assistant_name="rag-assistant-clevel", 
# )

# response = assistant.upload_file(
#     file_path="/Users/jdoe/Downloads/example_file.txt",
#     timeout=None
# )


# from pinecone import Pinecone
# from pinecone_plugins.assistant.models.chat import Message

# pc = Pinecone(api_key='PINECONE_API_KEY')

# assistant = pc.assistant.Assistant(assistant_name="rag-assistant-clevel")

# msg = Message(content="How old is the earth?")
# resp = assistant.chat(messages=[msg])

# print(resp["message"]["content"])

# # With streaming
# chunks = assistant.chat(messages=[msg], stream=True)

# for chunk in chunks:
#     if chunk:
#         print(chunk)