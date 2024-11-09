from dotenv import load_dotenv
import os
from instructions import *
from file_search import search
from pdf_util import * 
from vector_store_util import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_final_list(resume_list):
  load_dotenv()
  concatPdf = os.getenv("concatPdf")
  finalpdf_list = []
  logging.info(f"concat pdf  : {concatPdf} {type(concatPdf)}")
  if bool(concatPdf) == True:
    concat_pdf =concatenate_pdfs(resume_list)
    finalpdf_list.append(concat_pdf)
  else:
    logging.info(f"resume list  - {resume_list}")
    finalpdf_list = list(resume_list)
  logging.info(f"total file list - {len(finalpdf_list)}")
  return finalpdf_list 
      

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
    logging.info(f"processing the resumes {resume1} {resume2}")
    file_list = get_final_list([resume1,resume2])
    # index file into vector store
    logging.info(f"index files into vector store : {',' .join(file_list)} ")
    store_id = add_files_instore(vector_store,file_list)
    logging.info(f"post creating index  {store_id}")
    # search for comparative analysis
    # get the instructions to assistant 
    instructions , inst_file_id = get_instructions()
    logging.info(f"instruction file id  {inst_file_id}")
    logging.debug(f"instruction :  {instructions}")
    assistant_output = search([store_id],prompt,instructions)
    result = "\n".join(assistant_output)
    
    return result 
  
  
def format_resume_name(candidate_name):
  resume_name = candidate_name
  resume_name = resume_name.replace(" ","_")
  resume_name = resume_name + ".pdf"
  return resume_name
