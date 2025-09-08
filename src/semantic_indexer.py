import networkx as nx
import chromadb
from sentence_transformers import SentenceTransformer
from src import llm_service, spreadsheet_parser
import time

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./index")
collection = chroma_client.get_or_create_collection(name="spreadsheet_graph_semantics")


def format_subgraph_for_llm(workbook, graph, subgraph_nodes):
    if not subgraph_nodes:
        return ""
    subgraph = graph.subgraph(subgraph_nodes)
    result_nodes = [n for n, d in subgraph.out_degree() if d == 0]
    if not result_nodes:
        result_nodes = list(subgraph_nodes)
    result_node = result_nodes[0]
    output_lines = []
    def format_node_info(node):
        sheet_name, coord = node.split('!')
        cell = workbook[sheet_name][coord]
        formula = graph.nodes[node].get('formula', '')
        value = cell.value
        return f"{coord} [Value: {value}] {'Formula: ' + formula if formula else ''}"
    output_lines.append(f"Primary Concept: {format_node_info(result_node)}")
    output_lines.append("Dependencies:")
    predecessors = list(graph.predecessors(result_node))
    for p_node in predecessors:
        output_lines.append(f"  - {format_node_info(p_node)}")
    return "\n".join(output_lines)


def create_index_from_spreadsheet(file_path: str):
    print(f"\n_________________ Starting indexing for: {file_path} _________________")
    workbook, graph = spreadsheet_parser.build_dependency_graph(file_path)
    if not graph:
        print("Failed to build graph. Aborting for this file.")
        return

    key_nodes = [node for node, data in graph.nodes(data=True) if data.get('formula') and graph.in_degree(node) > 0]
    print(f"Found {len(key_nodes)} potential key nodes.")

    if not key_nodes:
        print("Warning: No key nodes found in this sheet. Nothing to index.")

    for i, node in enumerate(key_nodes):
        print(f"\n--- Processing node {i+1}/{len(key_nodes)}: {node} ---")
        ancestors = nx.ancestors(graph, node)
        ancestors.add(node)
        
        chunk_data = format_subgraph_for_llm(workbook, graph, ancestors)
        if not chunk_data:
            print(f"Skipping node {node} due to empty chunk data.")
            continue

        analysis = llm_service.analyze_chunk(chunk_data)
        if not analysis:
            print(f"LLM analysis failed for node {node}. Skipping.")
            continue
        
        print(f"LLM analysis successful for node {node}.")

        if 'keywords' in analysis and isinstance(analysis['keywords'], list):
            analysis['keywords'] = ', '.join(analysis['keywords'])

        document_to_embed = f"Concept: {analysis.get('concept')}. Description: {analysis.get('description')}"
        embedding = embedding_model.encode(document_to_embed).tolist()

        try:
            collection.add(
                embeddings=[embedding],
                documents=[chunk_data],
                metadatas=[{"file": file_path, "node": node, **analysis}],
                ids=[f"{file_path}_{node}"]
            )
            print(f"Successfully added node {node} to the index.")
        except Exception as e:
            print(f"Error adding node {node} to ChromaDB: {e}")

        
        if i < len(key_nodes) - 1: 
             print("Waiting 6.7 seconds to stay within 9 RPM rate limit...")
             time.sleep(6.7)
            
    print(f"\n--- Indexing complete for: {file_path} ---")
    
    from pathlib import Path

    print(f"\n--- Indexing complete for: {file_path} ---")
    
    Path('./index/.index_complete').touch()



def delete_index_for_file(file_path: str):
    """Deletes all records associated with a specific file from the index."""
    try:
        print(f"Deleting existing index entries for: {file_path}")
        collection.delete(where={"file": file_path})
        print("Deletion successful.")
    except Exception as e:
        print(f"Error deleting entries for {file_path}: {e}")

