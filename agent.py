import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

store_map_path = 'store_map.json'

def load_store_map(filepath='store_map.json'):
    with open(filepath, 'r') as f:
        return json.load(f)
    
def ask(question, stores):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=question,
        config=types.GenerateContentConfig(
            tools=[types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=stores
                )
            )]
        )
    )

    grounding = response.candidates[0].grounding_metadata
    if not grounding:
        print('[!] nenhuma fonte encontrada.')

    sources = {c.retrieved_context.title for c in grounding.grounding_chunks}
    print('[i] fontes:', *sources)

    return response.text

def main():
    store_map = load_store_map(store_map_path)
    stores = list(store_map.values())
   
    while True:
        question = input("Qual a sua dúvida sobre os editais? (ou digite 'sair' para encerrar): ")
        if question.lower() == 'sair':
            break
        answer = ask(question, stores)
        print("[i] resposta:", answer)

if __name__ == "__main__":
    main()