import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    PHI3_API_KEY = os.environ["PHI3_API_KEY"]  # API key
    # Text embedding deployment name
    TEXT_EMBEDDING_DEPLOYMENT_NAME = os.environ["TEXT_EMBEDDING_DEPLOYMENT_NAME"]
    AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]  # OpenAI API key
    # OpenAI endpoint
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
    # Azure search key
    SECRET_AZURE_SEARCH_KEY = os.environ["SECRET_AZURE_SEARCH_KEY"]
    # Azure search endpoint
    AZURE_SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
    INDEX_NAME = os.environ["INDEX_NAME"]  # Index name
    # PHI3_LOCATION = "azure"  # Location of Phi3
    PHI3_LOCATION = "azure"  # Location of Phi3 ~ # local # azure # port ~
    AZURE_OPENAI_GPT4_API_KEY = os.environ["AZURE_OPENAI_GPT4_API_KEY"]  # OpenAI GPT-4 API key
    
    GUARDIAN_NAME = "Rajesh Patel"  # Guardian name
    STUDENT_NAME = "Aryan Patel"  # Student name
    SCHOOL_NAME = "St. Xavier's School"  # School name