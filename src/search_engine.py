from sentence_transformers import SentenceTransformer
import chromadb
from src import llm_service

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./index")
collection = chroma_client.get_collection(name="spreadsheet_graph_semantics")

def search(query: str, top_n: int = 3):
    """Performs semantic search and formats the unique output."""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_n)
    
    formatted_results = []
    if not results['ids'][0]: return formatted_results

    for i in range(len(results['ids'][0])):
        metadata = results['metadatas'][0][i]
        document = results['documents'][0][i] 
        
        explanation = llm_service.generate_result_explanation(query, document)
        
        formatted_results.append({
            "Concept Name": metadata.get('concept'),
            "Location": f"'{metadata.get('file')}' -> Node('{metadata.get('node')}')",
            "Relevance": explanation,
            "Calculation Breakdown": document
        })
    return formatted_results
