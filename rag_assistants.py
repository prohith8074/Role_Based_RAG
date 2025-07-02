import os
from dotenv import load_dotenv
from summarize_context import chunk_retrieved_context, document_chunks, cohere_summarize
from opik_evaluation import evaluate_llm_response
from gemini_response import genai_response
from cohere_response import cohere_command_A_resopnse

from Pinecone_AI_Assistant import clevel_response, finance_response




# Milvus imports
try:
    from pymilvus import MilvusClient
    # Try to import embedding function, with fallback if not available
    try:
        from pymilvus.model.dense import CohereEmbeddingFunction
    except ImportError:
        # Fallback for older versions or different installations
        CohereEmbeddingFunction = None
    MILVUS_AVAILABLE = True
except ImportError:
    print("Milvus model not available, using fallback")
    MILVUS_AVAILABLE = False
    CohereEmbeddingFunction = None
    MilvusClient = None

# Qdrant imports
from qdrant_client import QdrantClient
import cohere

# Pinecone imports
from pinecone import Pinecone


# Simple Message class for Pinecone operations
class Message:

    def __init__(self, content):
        self.content = content


load_dotenv()


class EmployeeAssistant:
    """Employee RAG Assistant using Milvus"""

    def __init__(self):
        print("Initializing Employee Assistant...")

        # Initialize Cohere embedding function
        cohere_api = os.getenv("MILVUS_COHERE_API")
        if cohere_api and cohere_api != "default_key" and MILVUS_AVAILABLE and CohereEmbeddingFunction:
            try:
                self.ef = CohereEmbeddingFunction("embed-multilingual-v3.0",
                                                  api_key=cohere_api)
                print("Employee Assistant: Cohere embeddings initialized")
            except Exception as e:
                print(
                    f"Employee Assistant: Cohere embedding initialization failed: {e}"
                )
                self.ef = None
        else:
            print(
                "Employee Assistant: No valid Cohere API key found or CohereEmbeddingFunction not available"
            )
            self.ef = None

        # Initialize Milvus client
        uri = os.getenv("MILVUS_CLIENT_EMPLOYEE_URI")
        token = os.getenv("MILVUS_CLIENT_EMPLOYEE_TOKEN")

        if uri and token and MILVUS_AVAILABLE and MilvusClient and self.ef:
            try:
                self.client = MilvusClient(uri=uri, token=token)
                print(f"Employee Assistant: Connected to Milvus at {uri}")
            except Exception as e:
                print(
                    f"Employee Assistant: Milvus client initialization failed: {e}"
                )
                self.client = None
        else:
            print(
                "Employee Assistant: Milvus connection failed - missing credentials or embeddings"
            )
            self.client = None

        self.collection = "RAG_DB_Employee"

    def search_query(self, user_query):
        """Search for relevant documents"""
        if not self.client or not self.ef:
            print("Employee Assistant: Database or embeddings not available")
            return []

        try:
            print(f"Employee Assistant: Searching for: {user_query[:100]}...")
            queries = [user_query]
            
            # Check if embedding function is available
            if self.ef and hasattr(self.ef, 'encode_queries'):
                query_embeddings = self.ef.encode_queries(queries)
            else:
                print("Employee Assistant: Embedding function not available")
                return []

            results = self.client.search(collection_name=self.collection,
                                         data=query_embeddings,
                                         consistency_level="Strong",
                                         output_fields=["text"],
                                         limit=5)
            print(
                f"Employee Assistant: Found {len(results[0]) if results else 0} results"
            )
            return results
        except Exception as e:
            print(f"Employee Assistant search error: {e}")
            return []

    def document_retrieved_text(self, results):
        """Extract text from search results"""
        documents = []
        for result_list in results:
            for result in result_list:
                if 'entity' in result and 'text' in result['entity']:
                    documents.append(result['entity']['text'])

        # combined_text = " ".join(documents)
        text = " "
        for i in documents:
            text += "".join(i)
        # return text
        print(
            f"Employee Assistant: Retrieved {len(documents)} documents, {len(text)} characters"
        )
        print("documnted text",type(text))
        return text

    def get_response(self, query):
        """Get response for Employee queries"""
        print("Employee Assistant: Processing query...")
        search_results = self.search_query(query)
        document_text = self.document_retrieved_text(search_results)
        print("Document text:", document_text)
        print("Type of document_text:", type(document_text))
        
        #chunks = chunk_retrieved_context(document_text)
        # document_chunks_result = document_chunks(chunks)
        # summarized_context = cohere_summarize(document_chunks_result,query)

        response1 = evaluate_llm_response(document_text, query)
        print("Response generated evaluated:", response1)
        # response=cohere_summarize(chunks,query)
        response=genai_response(document_text,query)
        print("Response generated:", response)
        return f"\U0001F4CB **Employee Assistant:**\n\n{response}"
       
class EngineeringAssistant:
    """Engineering RAG Assistant using Milvus"""

    def __init__(self):
        print("Initializing Engineering Assistant...")

        # Initialize Cohere embedding function
        cohere_api = os.getenv("MILVUS_COHERE_API", "default_key")
        if cohere_api and cohere_api != "default_key" and MILVUS_AVAILABLE and CohereEmbeddingFunction:
            try:
                self.ef = CohereEmbeddingFunction("embed-multilingual-v3.0",
                                                  api_key=cohere_api)
                print("Engineering Assistant: Cohere embeddings initialized")
            except Exception as e:
                print(
                    f"Engineering Assistant: Cohere embedding initialization failed: {e}"
                )
                self.ef = None
        else:
            print(
                "Engineering Assistant: No valid Cohere API key found or CohereEmbeddingFunction not available"
            )
            self.ef = None

        # Initialize Milvus client
        uri = os.getenv("MILVUS_CLIENT_ENGINEERING_URI")
        token = os.getenv("MILVUS_CLIENT_ENGINEERING_TOKEN")

        if uri and token and MILVUS_AVAILABLE and MilvusClient and self.ef:
            try:
                self.client = MilvusClient(uri=uri, token=token)
                print(f"Engineering Assistant: Connected to Milvus at {uri}")
            except Exception as e:
                print(
                    f"Engineering Assistant: Milvus client initialization failed: {e}"
                )
                self.client = None
        else:
            print(
                "Engineering Assistant: Milvus connection failed - missing credentials or embeddings"
            )
            self.client = None

        self.collection = "RAG_DB_Engineering"

    def search_query(self, user_query):
        """Search for relevant documents"""
        if not self.client or not self.ef:
            print(
                "Engineering Assistant: Database or embeddings not available")
            return []

        try:
            print(
                f"Engineering Assistant: Searching for: {user_query[:100]}...")
            queries = [user_query]
            
            # Check if embedding function is available
            if self.ef and hasattr(self.ef, 'encode_queries'):
                query_embeddings = self.ef.encode_queries(queries)
            else:
                print("Engineering Assistant: Embedding function not available")
                return []

            results = self.client.search(collection_name=self.collection,
                                         data=query_embeddings,
                                         consistency_level="Strong",
                                         output_fields=["text"],
                                         limit=5)
            print(
                f"Engineering Assistant: Found {len(results[0]) if results else 0} results"
            )
            return results
        except Exception as e:
            print(f"Engineering Assistant search error: {e}")
            return []

    def document_retrieved_text(self, results):
        """Extract text from search results"""
        documents = []
        for result_list in results:
            for result in result_list:
                if 'entity' in result and 'text' in result['entity']:
                    documents.append(result['entity']['text'])

        # combined_text = " ".join(documents)
        text = " "
        for i in documents:
            text += "".join(i)
        # return text
        print(
            f"Engineering Assistant: Retrieved {len(documents)} documents, {len(text)} characters"
        )
        # return combined_text
        return text

    def get_response(self, query):
        """Get response for Engineering queries"""
        try:
            print("Engineering Assistant: Processing query...")
            search_results = self.search_query(query)

            if search_results and any(search_results):
                document_text = self.document_retrieved_text(search_results)

                if document_text.strip():
                    print(
                        "Engineering Assistant: Processing through summarization pipeline"
                    )
                    chunks = chunk_retrieved_context(document_text)
                    document_chunks_result = document_chunks(chunks)
                    summarized_context = cohere_summarize(document_chunks_result,query)

                    # document_chunks_result = document_chunks(chunks)
                    # summarized_context = cohere_summarize(
                    #     document_chunks_result)
                    response1 = evaluate_llm_response(summarized_context, query)
                    print("Response generated evaluated:", response1)
                    response=genai_response(chunks,query)
                    return f"🔧 **Engineering Assistant:**\n\n{response}"

            return "🔧 **Engineering Assistant:** I couldn't find relevant information in the Engineering knowledge base for your query. Please try rephrasing your question or check the technical documentation."

        except Exception as e:
            print(f"Engineering assistant error: {e}")
            return f"🔧 **Engineering Assistant Error:** An error occurred while processing your request: {str(e)}"


class HRAssistant:
    """HR RAG Assistant using Qdrant"""

    def __init__(self):
        print("Initializing HR Assistant...")

        # Initialize Qdrant client
        url = os.getenv("QDRANT_CLIENT_HR_URL")
        api_key = os.getenv("QDRANT_CLIENT_HR_API_KEY")

        if url and api_key:
            try:
                self.client = QdrantClient(url=url, api_key=api_key)
                print(f"HR Assistant: Connected to Qdrant at {url}")
            except Exception as e:
                print(f"HR Assistant: Qdrant connection failed: {e}")
                self.client = None
        else:
            self.client = None
            print(
                "HR Assistant: Qdrant connection failed - missing credentials")

        # Initialize Cohere for embeddings
        embed_api_key = os.getenv("QDRANT_COHERE_EMBEDDINGS_API_KEY", "")
        if embed_api_key:
            try:
                self.co = cohere.Client(embed_api_key)
                print("HR Assistant: Cohere embeddings initialized")
            except Exception as e:
                print(f"HR Assistant: Cohere embeddings failed: {e}")
                self.co = None
        else:
            self.co = None
            print("HR Assistant: Cohere embeddings failed - missing API key")

        self.model = "embed-english-v3.0"

    def search_query_in_database(self, query):
        """Search for relevant documents in Qdrant"""
        if not self.client or not self.co:
            print("HR Assistant: Database or embeddings not available")
            return ""

        try:
            print(f"HR Assistant: Searching for: {query[:100]}...")
            query_embeddings = self.co.embed(texts=[query],
                                             model=self.model,
                                             input_type="search_query",
                                             embedding_types=['float'])

            # Safely access embeddings
            if hasattr(query_embeddings, 'embeddings') and hasattr(query_embeddings.embeddings, 'float_'):
                query_vector = query_embeddings.embeddings.float_[0]
            else:
                query_vector = query_embeddings.embeddings[0]

            search_result = self.client.query_points(
                collection_name="RAG_HR",
                query=query_vector,
                limit=5).points

            document_list = [
                point.payload['document'] for point in search_result
            ]
            combined_text = " ".join(document_list)
            print(
                f"HR Assistant: Retrieved {len(document_list)} documents, {len(combined_text)} characters"
            )
            print(f"HR Assistant: RETRIEVED CONTEXT: {combined_text[:500]}..."
                  if len(combined_text) >
                  500 else f"HR Assistant: RETRIEVED CONTEXT: {combined_text}")
            return combined_text
        except Exception as e:
            print(f"HR Assistant search error: {e}")
            return ""

    def get_response(self, query):
        """Get response for HR queries"""
        try:
            print("HR Assistant: Processing query...")
            search_result = self.search_query_in_database(query)

            if search_result.strip():
                print(
                    "HR Assistant: Processing through summarization pipeline")
                # Process through summarization pipeline
                print(f"Retrieved context", search_result)
                chunks = chunk_retrieved_context(search_result)
                document_chunks_result = document_chunks(chunks)
                summarized_context = cohere_summarize(document_chunks_result,query)

                # Generate final response using Groq LLM
                response1 = evaluate_llm_response(summarized_context, query)
                print("Response generated evaluated:", response1)
                response=cohere_command_A_resopnse(chunks,query)
                return f"👥 **HR Assistant:**\n\n{response}"

            return "👥 **HR Assistant:** I couldn't find relevant information in the HR knowledge base for your query. Please try rephrasing your question or contact HR directly."

        except Exception as e:
            print(f"HR assistant error: {e}")
            return f"👥 **HR Assistant Error:** An error occurred while processing your request: {str(e)}"


class MarketingAssistant:
    """Marketing RAG Assistant using Qdrant"""

    def __init__(self):
        print("Initializing Marketing Assistant...")

        # Initialize Qdrant client
        url = os.getenv("QDRANT_CLIENT_MARKETING_URL", "")
        api_key = os.getenv("QDRANT_CLIENT_MARKETING_API_KEY", "")

        if url and api_key:
            try:
                self.client = QdrantClient(url=url, api_key=api_key)
                print(f"Marketing Assistant: Connected to Qdrant at {url}")
            except Exception as e:
                print(f"Marketing Assistant: Qdrant connection failed: {e}")
                self.client = None
        else:
            self.client = None
            print(
                "Marketing Assistant: Qdrant connection failed - missing credentials"
            )

        # Initialize Cohere for embeddings
        embed_api_key = os.getenv("QDRANT_COHERE_EMBEDDINGS_API_KEY", "")
        if embed_api_key:
            try:
                self.co = cohere.Client(embed_api_key)
                print("Marketing Assistant: Cohere embeddings initialized")
            except Exception as e:
                print(f"Marketing Assistant: Cohere embeddings failed: {e}")
                self.co = None
        else:
            self.co = None
            print(
                "Marketing Assistant: Cohere embeddings failed - missing API key"
            )

        self.model = "embed-english-v3.0"

    def search_query_in_database(self, query):
        """Search for relevant documents in Qdrant"""
        if not self.client or not self.co:
            print("Marketing Assistant: Database or embeddings not available")
            return ""

        try:
            print(f"Marketing Assistant: Searching for: {query[:100]}...")
            query_embeddings = self.co.embed(texts=[query],
                                             model=self.model,
                                             input_type="search_query",
                                             embedding_types=['float'])

            # Safely access embeddings
            if hasattr(query_embeddings, 'embeddings') and hasattr(query_embeddings.embeddings, 'float_'):
                query_vector = query_embeddings.embeddings.float_[0]
            else:
                query_vector = query_embeddings.embeddings[0]

            search_result = self.client.query_points(
                collection_name="RAG_Marketing",
                query=query_vector,
                limit=5).points

            document_list = [
                point.payload['document'] for point in search_result
            ]
            combined_text = " ".join(document_list)
            print(
                f"Marketing Assistant: Retrieved {len(document_list)} documents, {len(combined_text)} characters"
            )
            print(
                f"Marketing Assistant: RETRIEVED CONTEXT: {combined_text[:500]}..."
                if len(combined_text) > 500 else
                f"Marketing Assistant: RETRIEVED CONTEXT: {combined_text}")
            return combined_text
        except Exception as e:
            print(f"Marketing Assistant search error: {e}")
            return ""

    def get_response(self, query):
        """Get response for Marketing queries"""
        try:
            print("Marketing Assistant: Processing query...")
            search_result = self.search_query_in_database(query)

            if search_result.strip():
                print(
                    "Marketing Assistant: Processing through summarization pipeline"
                )
                chunks = chunk_retrieved_context(search_result)
                document_chunks_result = document_chunks(chunks)
                summarized_context = cohere_summarize(document_chunks_result,query)

                # #document_chunks_result = document_chunks(chunks)
                # #summarized_context = cohere_summarize(document_chunks_result)
                
                response1 = evaluate_llm_response(summarized_context, query)
                print("Response generated evaluated:", response1)
                response=cohere_command_A_resopnse(chunks,query)
                return f"📈 **Marketing Assistant:**\n\n{response}"

            return "📈 **Marketing Assistant:** I couldn't find relevant information in the Marketing knowledge base for your query. Please try rephrasing your question or check the marketing resources."

        except Exception as e:
            print(f"Marketing assistant error: {e}")
            return f"📈 **Marketing Assistant Error:** An error occurred while processing your request: {str(e)}"


class FinanceAssistant:
    """Finance RAG Assistant using Pinecone"""
    def get_response(self, query):
        """Get response for C-Level Executive queries"""
        try:
            print("C-Level Assistant: Processing query...")
            response=finance_response(query)

            return f"🏢 **Finance  Assistant:**\n\n{response}"

            # return "🏢 **Finance  Assistant:** I couldn't find relevant information in the executive knowledge base for your query. Please try rephrasing your question or consult the strategic documentation."

        except Exception as e:
            print(f"Finance assistant error: {e}")
            return f"🏢 **Finance Assistant Error:** An error occurred while processing your request: {str(e)}"

    
    
    # return "💰 **Finance Assistant:** I couldn't find relevant information in the Finance knowledge base for your query. Please try rephrasing your question or consult the financial documentation."

        

class CLevelAssistant:
    """C-Level Executive RAG Assistant using Pinecone"""

    def get_response(self, query):
        """Get response for C-Level Executive queries"""
        try:
            print("C-Level Assistant: Processing query...")
            # search_result = self.search_query_in_database(query)
            response=clevel_response(query)
           
            return f"🏢 **C-Level Executive Assistant:**\n\n{response}"

           
        except Exception as e:
            # print(f"C-Level assistant error: {e}")
            return f"🏢  **C-Level Executive Assistant Error:** An error occurred while processing your request, try again"
