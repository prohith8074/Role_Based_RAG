from langchain.text_splitter import RecursiveCharacterTextSplitter
import cohere
import os
from dotenv import load_dotenv

load_dotenv()


def chunk_retrieved_context(text, chunk_size=512, chunk_overlap=50):
    """Splits retrieved context into overlapping chunks for better LLM processing."""
    if not text or not text.strip():
        print("No text provided for chunking")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        )

    chunks = splitter.split_text(text)
    print(f"Created {len(chunks)} chunks from {len(text)} characters")
    print("chunks type",type(chunks))
    return chunks


def document_chunks(chunks):
    """Convert chunks to document format for Cohere"""
    if not chunks:
        print("No chunks provided for document conversion")
        return []

    document_chunked = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():  # Only add non-empty chunks
            document_chunked.append({"data": {"text": chunk.strip()}})

    print(f"Converted {len(document_chunked)} chunks to document format")
    return document_chunked


def cohere_summarize(documents,query):
    """Summarizes the text using Cohere's summarization model."""
    if not documents:
        print("No documents provided for summarization")
        return "No content available for summarization."
 
    api_key = os.getenv("COHERE_SUMMARIZE_API_KEY", "default_key")


    system_message = """## Task and Context
You will receive a query and the  long text  from a document that are  retrieved from vector databse. 
As the assistant, you must generate summries  to given long text that should contain 
all the information to answer the query in detail, only from the summaries that you generates. Ensure that the 
summarization of the text is accurate and truthful, regardless of their complexity."""

    message=f""" 
    user_query: {query},
    text: {documents} """
    try:
        print(f"Summarizing {len(documents)} documents using Cohere...")
        co = cohere.ClientV2(api_key=api_key)
        response = co.chat(
            model="command-r-03-2024",
            documents=documents,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ],
        )
        # print(f"Cohere response received: {response}")
        # Safe access to response content
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            if isinstance(response.message.content, list) and len(response.message.content) > 0:
                summarized_text = response.message.content[0].text
            else:
                summarized_text = str(response.message.content)
        else:
            summarized_text = str(response)
        print(
            f"Cohere summarization successful: {len(summarized_text)} characters"
        )
        print(f"Cohere response received: {summarized_text}")
        return summarized_text

    except Exception as e:
        print(f"Cohere summarization error: {e}")
        # Fallback to simple concatenation if Cohere fails - return full content
        if isinstance(documents, list):
            combined_text = " ".join(
                [doc.get("data", {}).get("text", "") for doc in documents])
            print(
                f"Using fallback summarization: {len(combined_text)} characters"
            )
            return combined_text  # Return full content without truncation
        full_content = str(documents)
        print(f"Using fallback summarization: {len(full_content)} characters")
        return full_content  # Return full content without truncation
