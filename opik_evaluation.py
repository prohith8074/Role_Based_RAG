import os
from dotenv import load_dotenv

load_dotenv()

# Set environment variables with fallbacks
groq_api_key = os.getenv("GROQ_API_KEY", "default_key")
opik_api_key = os.getenv("OPIK_API_KEY", "")

# Opik evaluation setup - make optional to prevent blocking
OPIK_AVAILABLE = False
try:
    # Only configure if API key is explicitly provided
    if opik_api_key and opik_api_key.strip() and opik_api_key != "":
        os.environ["OPIK_API_KEY"] = opik_api_key
        if groq_api_key and groq_api_key != "default_key":
            os.environ["GROQ_API_KEY"] = groq_api_key
        os.environ["OPIK_PROJECT_NAME"] = "RAG"
        
        import opik
        opik.configure(use_local=False, automatic_approvals=True)
        
        import litellm
        from litellm.integrations.opik.opik import OpikLogger
        
        opik_logger = OpikLogger()
        litellm.callbacks = [opik_logger]
        OPIK_AVAILABLE = True
        print("Opik monitoring enabled")
    else:
        print("Opik API key not provided - running without monitoring")
except Exception as e:
    print(f"Opik configuration failed: {e} - continuing without monitoring")
    import litellm
    OPIK_AVAILABLE = False
    print("Opik monitoring disabled")

def evaluate_llm_response(context, user_query):
    """Generate LLM response using Groq with context and query"""
    # if not context or not context.strip():
    #     return "⚠️ **No Context Available**: Unable to find relevant information in the knowledge base for your query."
    
    # if not user_query or not user_query.strip():
    #     return "⚠️ **Invalid Query**: Please provide a valid question."
    
    print(f"Groq LLM: Processing query with {len(context)} characters of context")
    
    prompt = f"""
Please answer the query in detail based on the provided context only.

Context Information:
{context}

User Query: {user_query}

Instructions:
- Answer based ONLY on the provided context
- If the context doesn't contain sufficient information to answer the query, clearly state that
- Provide detailed and helpful responses when possible
- Maintain professional tone appropriate for business environment
- Reference specific information from the context when applicable
- If the query asks about multiple topics, address each part systematically
"""

    try:
        if groq_api_key == "default_key":
            print("Groq LLM: No API key available, using context-based fallback")
            return f"**Context-Based Response:**\n\nBased on the available information: {context[:500]}{'...' if len(context) > 500 else ''}\n\nTo get a comprehensive AI-generated response, please configure the GROQ_API_KEY environment variable."
        
        print("Groq LLM: Calling API...")
        response = litellm.completion(
            model="groq/llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        
        # Safe access to response content
        if hasattr(response, 'choices') and response.choices:
            if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                result = response.choices[0].message.content
            else:
                result = str(response.choices[0])
        else:
            result = str(response)
            
        if result:
            print(f"Groq LLM: Successfully generated response ({len(result)} characters)")
            return result
        else:
            return "⚠️ **LLM Response Error**: No content received from API"
        
    except Exception as e:
        print(f"Groq LLM error: {e}")
        # Fallback with context information
        return f"⚠️ **LLM Processing Error**: {str(e)}\n\n**Based on available context:**\n{context[:500]}{'...' if len(context) > 500 else ''}"
