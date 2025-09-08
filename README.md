# Semantic Spreadsheet Search

Semantic Spreadsheet Search is a Python application that enables semantic search and analysis of spreadsheet files (Excel workbooks) using Large Language Models (LLMs) and vector embeddings. It builds a dependency graph from spreadsheet formulas, extracts key concepts, and indexes them for semantic retrieval.

## Features
- Semantic Content Understanding
- Natural Language Query Processing(Conceptual, Functional and Comparative)
- Intelligent Result Ranking & Output
- Supports Multi-Sheet Understanding
- Handle real-time updates as content changes
- Handles edge cases like empty queries/ irrelevant searches

## Project Structure
```
├── check_index.py
├── config.py
├── main.py
├── requirements.txt
├── watcher.py
├── data/
│   ├── Test_Financial_Model.xlsx
│   └── Test_Sales_Dashboard.xlsx
├── index/ 
│   └── chroma.sqlite3
├── src/
│   ├── __init__.py
│   ├── llm_service.py
│   ├── search_engine.py
│   ├── semantic_indexer.py
│   └── spreadsheet_parser.py
```

## Installation
1. **Clone the repository:**
   ```powershell
   git clone <repo-url>
   cd semantic-spreadsheet-search
   ```
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Create a .env file in the project root and add your API key**
    GEMINI_API_KEY="---Your key here---"
## Usage
1. **Prepare your Excel files:**
   Place `.xlsx` files in the `data/` directory.

2. **Run the main script:**
   ```powershell
   python main.py
   ```
   This will index the spreadsheets and allow semantic search.

**Please Note: If you want to re-index manually, delete the index folder in the project first and then perform step 2**

3.  **Once indexing is done/ already exists, search bar pops up in terminal/CLI, type your query and press enter**

Sample queries:

- Show me cost-related formulas
- Where are my growth rates?
-  Profit killers
- Show percentage calculations
- Find average formulas
- Time series data

Sample search query and result(1 out of 3 displayed here):

Search> Find all profitability metrics

--- Search Results ---

========== Result 1 ==========
Concept: Profitability Metric Derivation
Location: './data\Test_Financial_Model.xlsx' -> Node('3-Year Forecast!C9')

Relevance: This data is a relevant match because C8 calculates a form of profit (the difference between two financial figures), and C9 then derives a value as a percentage of that profit, which are both components or calculations directly related to profitability metrics.

--- Calculation Breakdown ---
Primary Concept: C9 [Value: =C8*0.2] Formula: =C8*0.2
Dependencies:
  - C8 [Value: =C6-C7] Formula: =C6-C7

  ==============================


4. **Open a separate terminal simultaneously and run script for watcher**

```powershell
   python watcher.py
   ```
Observe the initial state of watcher:

Watching for changes in .xlsx files... 


5. **Open any sheet included in the data folder , make some changes in them and save**


Observe the watcher terminal now. You should get a message similar to the message below:

--- Detected change in: {modified_file_path} ---
Deleting existing index entries for: {modified_file_path}
Deletion successful.
--- Triggering re-indexing for: {modified_file_path} ---

...................{Entire indexing process occurs}...................

modified_file_path:path of the sheet changed in the project
## How It Works
- **Dependency Graph:**
  - The parser (`spreadsheet_parser.py`) builds a directed graph of cell dependencies based on formulas.
- **Key Node Extraction:**
  - Nodes with formulas and dependencies are identified as key concepts.
- **LLM Analysis:**
  - Each key node and its subgraph are summarized and analyzed by an LLM (see `llm_service.py`).
- **Embedding & Indexing:**
  - Semantic embeddings are generated and stored in ChromaDB for fast retrieval.
- **Search:**
  - The search engine (`search_engine.py`) enables semantic queries over indexed concepts.

## Configuration
- Edit `config.py` to adjust model settings, paths, or other parameters.

## Requirements
- Python 3.8+
- See `requirements.txt` for all Python package dependencies.

