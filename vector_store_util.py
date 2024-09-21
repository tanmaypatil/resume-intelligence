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
    return vector_store.id

def search_vector_store(store_name):
    logging.info(f"searching store {store_name}")
    vector_stores = client.beta.vector_stores.list()
    stores = [  vs  for vs in vector_stores if vs.name == store_name  ]
    if stores is not None:
      store_len = len(stores)
      store_id = stores[0].id
      logging.info(f"store name exists {store_name}:{store_id}")
    return store_len
