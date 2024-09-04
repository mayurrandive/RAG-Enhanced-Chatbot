from config import Config
from langchain_openai import AzureOpenAIEmbeddings
# import VectorizedQuery
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json

def search_documents(query):
    embeddings = AzureOpenAIEmbeddings(
        api_key=Config.AZURE_OPENAI_API_KEY,
        model=Config.TEXT_EMBEDDING_DEPLOYMENT_NAME,
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
    )
    search_client = SearchClient(
        endpoint=Config.AZURE_SEARCH_ENDPOINT,
        index_name=Config.INDEX_NAME,
        credential=AzureKeyCredential(Config.SECRET_AZURE_SEARCH_KEY)
    )
    query_embedding = embeddings.embed_query(query)
    vector_query = VectorizedQuery(
        vector=query_embedding,
        fields='descriptionVector',
        k_nearest_neighbors=1)

    selectedFields = [
        'docTitle',
        'description',
        'descriptionVector',
    ]

    results = search_client.search(
        search_text=query,
        select=selectedFields,
        vector_queries=[vector_query],
        top=3
    )
    i =0
    for result in results:
        i+=1
        with open(f"search_res_{i}.txt", 'w') as file:
            file.write(json.dumps(result, indent=2))



if __name__ == '__main__':
    query = "What does a team game mean?"
    search_documents(query)
