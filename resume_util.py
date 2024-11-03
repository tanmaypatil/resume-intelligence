from dotenv import load_dotenv
import os
from file_search import search,add_files
from pdf_util import * 
from vector_store_util import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def resume_search(resume1,resume2,prompt):
    logging.info(f"resume search {prompt}")
    # index resume1 and resume2
    result = ""
    file_list = [resume1,resume2]
    # create vector store 
    load_dotenv()
    vector_store_str = os.getenv("vector_store_resume")
    # check if store exists , if not skip creation 
    store_len,store_id,vector_store = search_vector_store(vector_store_str)
    logging.info(f"store_len {store_len} for {vector_store_str}")
    if store_len == 0:
      vector_store = create_vector_store(vector_store_str)
      logging.info(f"create vector store {vector_store.name}:{vector_store.id}")
    # concatenate resumes - openapi requires single file
    logging.info(f"concatenating the resumes {resume1} {resume2}")
    concat_pdf =concatenate_pdfs(resume1,resume2)
    logging.info(f"concatenated resume {concat_pdf}")
    file_list = [concat_pdf]
    # index file into vector store
    logging.info(f"index into vector store {file_list} ")
    store_id = add_files_instore(vector_store,file_list)
    logging.info(f"post creating index  {store_id}")
    # search for comparative analysis
    assistant_output = search([store_id],prompt)
    result = "\n".join(assistant_output)
    
    return result 
  
  
def format_resume_name(candidate_name):
  resume_name = candidate_name
  resume_name = resume_name.replace(" ","_")
  resume_name = resume_name + ".pdf"
  return resume_name
