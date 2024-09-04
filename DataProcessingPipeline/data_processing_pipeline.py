from get_chunks import get_chunks
from get_data import get_pdfs
from create_embeddings import create_embeddings

def data_processing_pipeline():
    # start loading data

    documents = get_pdfs()
    print("Total number of documents: ", len(documents))
    chunks = get_chunks(documents)
    print("Total number of chunks: ", len(chunks))
    create_embeddings(chunks)
    print("Embeddings created!")
    print("Data processing pipeline completed!")

    
if __name__ == "__main__":
    data_processing_pipeline()