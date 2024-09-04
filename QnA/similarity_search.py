from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from config import Config
import json


def similarity_search(query: str = None):

    embeddings = AzureOpenAIEmbeddings(
        api_key=Config.AZURE_OPENAI_API_KEY,
        model=Config.TEXT_EMBEDDING_DEPLOYMENT_NAME,
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
    )

    with open("queries/emddedings_search.json", "w") as f:
        json.dump(str(embeddings), f, indent=4)

    vectordb = FAISS.load_local(
        './faiss_index_ml_papers',
        embeddings,
        allow_dangerous_deserialization=True,
    )

    res = vectordb.similarity_search_with_relevance_scores(query, k=10)

    doc = ""
    for i in res:
        if (i[1] < 0.65):
            break
        doc += str(i[0].page_content) + '\n\n'

    res2 = []
    for i in res:
        res2.append({"Document": str(i[0].page_content), "Similarity Score": i[1]})

    with open("./queries/similarity_search.json", "w") as f:
        json.dump(res2, f, indent=4)

    return doc
