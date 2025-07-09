
from pymilvus.model.dense import CohereEmbeddingFunction
from pymilvus import MilvusClient

# Initialize Cohere embedding function
COHERE_API_KEY = "<Your API key>"
ef = CohereEmbeddingFunction("embed-multilingual-v3.0", api_key=COHERE_API_KEY)

# Connect to Zilliz Cloud with Public Endpoint and API Key
client_engineering = MilvusClient(
    uri="Your <Milvus account  URI>",
    token="<Your Milvus account token")
#--------------------------------------------------------------------------------------------------------------------------------------

# Create a Collection 
COLLECTION = "<Collection Name>"
if client.has_collection(collection_name=COLLECTION):
    client.drop_collection(collection_name=COLLECTION)
client.create_collection(
    collection_name=COLLECTION,
    dimension=ef.dim,
    auto_id=True)

chunk=''
with open("<path to the employee summarized chunks> ",'r') as f:
  chunk=json.load(f)
# docs_embeddings = ef.encode_documents(chunk)

for i in range(len(chunk)):
  data=[chunk[i]['text']+chunk[i]["summary"]]
  embeddings = cohere_client.embed(
        texts=[chunk[0]["summary"]],
        model=COHERE_MODEL_NAME,
        input_type="search_document",
        truncate="END",
    ).embeddings
    

