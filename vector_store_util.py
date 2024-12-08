from openai import OpenAI
from typing import List
import logging
import os
from dotenv import load_dotenv
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

load_dotenv()
key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=key)


def delete_vector_store(store_name: str):
    logging.info(f"deleting store {store_name}")
    vector_stores = client.beta.vector_stores.list()
    stores = [vs.id for vs in vector_stores]
    if stores is not None:
        store_id = stores[0].id
    logging.info(f"deleting ${store_name}:{store_id}")
    return store_id


def create_vector_store(store_name: str):
    logging.info(f"creating store {store_name}")
    vector_store = client.beta.vector_stores.create(name=store_name)
    logging.info(f"creating store : store id {vector_store.id}")
    return vector_store


def search_vector_store(store_name: str):
    store_len = 0
    logging.info(f"searching store {store_name}")
    vector_stores = client.beta.vector_stores.list()
    stores = [vs for vs in vector_stores if vs.name == store_name]
    logging.info(f"search_vector_store {store_len}")
    if stores is not None and len(stores) > 0:
        store_len = len(stores)
        store_id = stores[0].id
        logging.info(f"store name exists {store_name}:{store_id}")
        return store_len, store_id, stores[0]
    else:
        return 0, None, None

def store_mapping(file_arr : list):
    with open('.\\system_config\\file_ids.json', 'w') as f:
      json.dump(file_arr, f)

def add_files_instore(vector_store: object, files: List[str], base_path='.\\resumes', max_chunk_size_tokens :int =800,
                      chunk_overlap_tokens :int =400):
    """Add files into a existing vector store"""
    file_dict = {}
    file_arr = []
    try:
        # Adding a files into existing store
        logging.info(
            f"Adding file into a existing store id :{vector_store.id}")
        # Upload files and add them to the vector store
        file_ids = []
        
        for file_path in files:
            file_path = f'{base_path}\\{file_path}'
            with open(file_path, "rb") as file:
                logging.info(f"Adding file  : {file_path}")
                file_dict = {}
                uploaded_file = client.files.create(
                    file=file, purpose="assistants")
                file_ids.append(uploaded_file.id)
                # add the mapping of file path and file id
                file_dict["file_id"] = uploaded_file.id
                file_dict["pdf_name"] = file_path
                file_arr.append(file_dict)
                logging.info(
                    f"Adding file  : {file_path} , file id : {uploaded_file.id}")

        logging.info(
            f" max_chunk_size_tokens :{max_chunk_size_tokens}  chunk_overlap_tokens :{chunk_overlap_tokens}")
        # Add files to the vector store
        file_batch = client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store.id,
            file_ids=file_ids,
            chunking_strategy= {
                "type" : "static",
                "static" : {
                "max_chunk_size_tokens" : max_chunk_size_tokens ,
                "chunk_overlap_tokens" : chunk_overlap_tokens
                }
            }
        )

        logging.info(f"Added {len(file_ids)} files to the vector store.")
        logging.info(f"File batch status: {file_batch.status}")
        logging.debug(f"File counts: {file_batch.file_counts}")
        
        # store the file id , file path mapping in json file
        store_mapping(file_arr)
        return vector_store.id
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None


def delete_vector_store_files(store_name):
    len_store, store_id, _ = search_vector_store(store_name)
    # get the list of files
    vector_store_files = client.beta.vector_stores.files.list(
        vector_store_id=store_id)
    ids = [v.id for v in vector_store_files]
    print(f"file ids : {','.join(ids)} ")
    for id in ids:
        deleted_vector_store_file = client.beta.vector_stores.files.delete(
            vector_store_id=store_id,
            file_id=id)
        print(
            f" vector store : {store_name}, file id {id} : {deleted_vector_store_file}")
    return len(ids)


def get_vector_store_file_count(store_name):
    len_store, store_id, _ = search_vector_store(store_name)
    # get the list of files
    vector_store_files = client.beta.vector_stores.files.list(
        vector_store_id=store_id)
    ids = [v.id for v in vector_store_files]
    return (len(ids), ids)
