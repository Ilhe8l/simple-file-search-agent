from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

pdf_folder = './editais'
store_map = {}

def save_store_map(store_map, filepath='store_map.json'):
    with open(filepath, 'w') as f:
        json.dump(store_map, f)

def create_file_search_store(pdf_path):
    store = client.file_search_stores.create()
    generated_name = store.name

    upload_op = client.file_search_stores.upload_to_file_search_store(
        file_search_store_name=generated_name,
        file=pdf_path
    )

    while not upload_op.done:
        upload_op = client.operations.get(upload_op)

    return store.name

def main():
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]
            store_name = create_file_search_store(pdf_path)
            store_map[pdf_name] = store_name
            print(f'[i] file search criado para {pdf_name}: {store_name}')
    save_store_map(store_map)

if __name__ == "__main__":
    main()