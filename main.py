import os
from src import semantic_indexer, search_engine

def run_indexing():
    """Indexes all .xlsx files in the data directory."""
    
    if os.path.exists('./index/.index_complete'):
        print("A complete index already exists. Skipping indexing.")
        return
        
    print("Starting indexing process...")
    data_dir = './data'
    if not os.path.exists(data_dir):
        print(f"ERROR!!!: Directory '{data_dir}' not found. Please create it and add spreadsheets.")
        return
        
    for filename in os.listdir(data_dir):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(data_dir, filename)
            semantic_indexer.create_index_from_spreadsheet(file_path)

def run_search_cli():
    """Starts the interactive search command-line interface."""
    print("\n--- Graph-Based Semantic Spreadsheet Search ---")
    print("Type your query or 'exit' to quit.")
    while True:
        query = input("\nSearch> ")
        if query.lower() == 'exit':
            break
        
        results = search_engine.search(query)
        
        if not results:
            print("No relevant results found.")
        else:
            print("\n--- Search Results ---")
            for i, res in enumerate(results, 1):
                print(f"\n========== Result {i} ==========")
                print(f"Concept: {res['Concept Name']}")
                print(f"Location: {res['Location']}")
                print(f"\nRelevance: {res['Relevance']}")
                print(f"\n--- Calculation Breakdown ---")
                print(res['Calculation Breakdown'])
                print("==============================")

if __name__ == '__main__':
    run_indexing()
    run_search_cli()