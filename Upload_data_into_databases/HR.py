from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import cohere


from qdrant_client import QdrantClient
#--------------------HR Data Cluster -----------------------------------
client = QdrantClient(
    url="<Your Qdrant client url",
    api_key="<Your api key>",
)
print(qdrant_client.get_collections())



# create a collection  -------Marketing Data-----------------

client.create_collection(
     collection_name="<Collection Name>",
     vectors_config=VectorParams(size=1024, distance=Distance.DOT),
 )


#Cohere model for Embedding
co = cohere.Client("< Cohere API key> ")
model="embed-english-v3.0"

def read_data(path):
  text_data=[]
  with open("path", "r") as f:
    text = f.read()
    text_data.append(text)
  return text_data

#Documents Embeddings (data) 
documents=read_data("<path to the HR summarized chunks>")
doc_embeddings = co.embed(texts=documents,
                           model=model,
                           input_type="search_document",
                           embedding_types=['float'])
operation_info = client.upsert(
    collection_name="<Collection Name>",
    points=points
)
