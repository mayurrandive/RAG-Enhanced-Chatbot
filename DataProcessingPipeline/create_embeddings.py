from IPython.display import clear_output
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
import sys
sys.path.append("..")
from config import Config
import ollama



# we create the embeddings if they do not already exist in the input folder
def create_embeddings(texts):
    if not os.path.exists('./embeddings' + '/index.faiss'):

        embeddings = AzureOpenAIEmbeddings(
            api_key=Config.AZURE_OPENAI_API_KEY,
            model=Config.TEXT_EMBEDDING_DEPLOYMENT_NAME,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )

        # create embeddings and DB
        vectordb = FAISS.from_documents(
            documents=texts,
            embedding=embeddings
        )

        # persist vector database
        # save in output folder
        vectordb.save_local(f"./faiss_index_ml_papers")

    clear_output()
