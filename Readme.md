# Mock Server Setup for Parent Bot in Teams TFL Account  
   
This README will help you set up the mock server made for the parent bot inside Teams TFL account.  
   
## Definition of Terms  
- **RAG Bot**: Retrieval-Augmented Generation bot  
- **SLM (phi3)**: Specialized Language Model (phi3)  
- **Prompt**: The initial input provided to the language model for generating responses  
   
## Environment Variables  
Fill the below environment variables into the `.env` file:  
```  
AZURE_OPENAI_ENDPOINT=<text-embedding-endpoint>  
TEXT_EMBEDDING_DEPLOYMENT_NAME=<deployed embedding model name>  
   
# Below are not necessary as we have used local vectordb for searching  
AZURE_OPENAI_API_KEY=SECRET  
AZURE_SEARCH_KEY=  
AZURE_SEARCH_ENDPOINT=  
INDEX_NAME='data'  
PHI3_API_KEY=  
```  
   
## Setup Instructions  
   
1. **Create a Python Virtual Environment**  
    ```sh  
    pip install virtualenv  
    virtualenv env  
    ```  
   
2. **Activate the Virtual Environment**  
    - For macOS/Linux:  
        ```sh  
        source env/bin/activate  
        ```  
    - For Windows:  
        ```sh  
        env\Scripts\activate  
        ```  
   
3. **Install Dependencies**  
    ```sh  
    pip install -r requirements.txt  
    ```  
   
4. **Add Sample Data**  
    - Add sample data PDFs into the `SchoolResources` folder.  
   
5. **Setting Up phi3 Locally**  
    - Download Ollama from the official website. This might require Docker to install. Follow the instructions provided.  
   
6. **Run phi3 Using Ollama**  
    ```sh  
    ollama run phi3  
    ```  
    - This will start phi3 on `localhost:11434`.  
   
7. **Modify Initial Prompt**  
    - You can modify the initial prompt in the `prompt_template.py` file.  
   
8. **Run Data Processing Pipeline**  
    - Run the data processing pipeline Python file to store vector embeddings of PDFs into vectordb.  
    - You can find it inside the `DataProcessingPipeline` folder.  
   
9. **Sample Questions**  
    - Some sample questions are listed in the `Sample_Questions.md` file.  
   
10. **Run the Server**  
    ```sh  
    flask --app app.py --debug run  
    ```  
    - The server will start on `127.0.0.0:5000/api/message`.  
   
## Input Format  
The format for input must be:  
```json  
{  
    "messages": [  
        {  
            "role": "user",  
            "content": [  
                {  
                    "type": "text",  
                    "text": "Hi"  
                }  
            ]  
        }  
    ]  
}  
```  