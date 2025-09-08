import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import time
import random


load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

def analyze_chunk(chunk_data: str):
    """
    Asks Gemini to analyze a chunk, with exponential backoff for rate limits.
    """
    if not model:
        print("Model not initialized.")
        return None

    prompt = f"""
    You are a financial and business analyst. Analyze the following spreadsheet data chunk,
    which represents a calculation tree.
    
    Identify the core business concept (e.g., "Revenue Growth", "Gross Margin Calculation").
    Provide a concise, one-sentence natural language description of what this data represents.
    List 5-10 relevant keywords and synonyms for semantic search.
    
    Format your response as a single, clean JSON object with three keys: "concept", "description", "keywords".

    Data Chunk:
    ---
    {chunk_data}
    ---
    """
    
    retries = 5
    delay = 4
    for i in range(retries):
        try:
            response = model.generate_content(prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned_response)
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit hit. Retrying in {delay} seconds... (Attempt {i+1}/{retries})")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
            else:
                print(f"An unexpected error occurred: {e}")
                return None
    
    print("All retries failed due to rate limiting.")
    return None

def generate_result_explanation(query: str, result_data: str):
    """
    Asks Gemini to explain why a search result is relevant to the user's query.
    """
    if not model:
        print("Model not initialized. Cannot generate explanation.")
        return "Model not available."

    prompt = f"""
    A user searched for: "{query}"
    We found the following spreadsheet calculation tree as a result:
    ---
    {result_data}
    ---
    In one sentence, explain why this data is a relevant match for the user's search query.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating explanation with Gemini: {e}")
        return "Could not generate an explanation for this result."
    
    