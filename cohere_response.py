# pip install cohere

import cohere
import json

# Get your free API key: https://dashboard.cohere.com/api-keys
co = cohere.ClientV2(api_key="iykpfAspIP148Rui6mBxw7dFAVanQFpgjoUTjYqB")




# Add the user message
def cohere_command_A_resopnse(context,query):
    """Generate a response using Cohere's chat model."""
    # if not context or not context.strip():
    #     return "⚠️ **No Context Available**: Unable to find relevant information in the knowledge base for your query."
    
    # if not user_query or not user_query.strip():
    #     return "⚠️ **Invalid Query**: Please provide a valid question."
    
    print("Cohere LLM: Processing query...")
    message = f"""You are an helpful assistant. 
              You will be given a context and based upon that answer the user's query in detail.

                query: {query}
                context: {context}
"""
    # Generate the response
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": message}],
    )
    #    messages=[cohere.UserMessage(content=message)])
    return response.message.content[0].text
# print(response.message.content[0].text)


