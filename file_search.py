from openai import OpenAI
from typing import List
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI()

def add_files(vector_store_name: str, files: List[str]):
    """Create a new vector store and add files to it."""
    try:
        # Create a new vector store
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
        logging.info(f"Created vector store: {vector_store_name}")

        # Upload files and add them to the vector store
        file_ids = []
        for file_path in files:
            with open(file_path, "rb") as file:
                uploaded_file = client.files.create(file=file, purpose="assistants")
                file_ids.append(uploaded_file.id)
        
        # Add files to the vector store
        file_batch = client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store.id,
            file_ids=file_ids
        )

        logging.info(f"Added {len(file_ids)} files to the vector store.")
        logging.info(f"File batch status: {file_batch.status}")
        logging.debug(f"File counts: {file_batch.file_counts}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", err=True)
