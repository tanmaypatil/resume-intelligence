from openai import OpenAI
from typing import List
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from readProp import *

key = readProperties("OPENAI_KEY")
client = OpenAI(api_key=key)

def delete_vector_store(store_name):
    logging.info(f"deleting store {store_name}")
    vector_stores = client.beta.vector_stores.list()
    stores = [  vs.id for vs in vector_stores ]
    if stores is not None:
      store_id = stores[0].id
    logging.info(f"deleting ${store_name}:{store_id}")
    return store_id     
 
def create_vector_store(store_name):
    logging.info(f"creating store {store_name}")
    vector_store = client.beta.vector_stores.create(name=store_name)
    logging.info(f"creating store : store id {vector_store.id}")
    return vector_store

def search_vector_store(store_name):
    store_len = 0
    logging.info(f"searching store {store_name}")
    vector_stores = client.beta.vector_stores.list()
    stores = [  vs  for vs in vector_stores if vs.name == store_name  ]
    logging.info(f"search_vector_store {store_len}")
    if stores is not None and len(stores) > 0 :
      store_len = len(stores)
      store_id = stores[0].id
      logging.info(f"store name exists {store_name}:{store_id}")
      return store_len,store_id,stores[0]
    else:
      return 0,None,None

def add_files_instore(vector_store: object, files: List[str]):
    """Add files into a existing vector store"""
    try:
        # Adding a files into existing store
        logging.info(f"Adding file into a existing store id :{vector_store.id}")
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
        return vector_store.id
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", err=True)
        return None      

