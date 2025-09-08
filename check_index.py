import chromadb

print("--- Checking ChromaDB Index ---")

try:
    
    chroma_client = chromadb.PersistentClient(path="./index")
    
    collection = chroma_client.get_collection(name="spreadsheet_graph_semantics")
    
    count = collection.count()
    
    print(f" Success! Found the collection.")
    print(f"Number of items in index: {count}")
    
    if count > 0:
        print("\nHere's a sample of what's inside:")
        print(collection.peek())
    else:
        print("\n The index is empty. This is why you're not getting any search results.")
        
except Exception as e:
    print(f"\n An error occurred: {e}")
    print("This might mean the index or collection doesn't exist yet.")

print("--- Check complete ---")