from dotenv import load_dotenv
import os
from instructions import *
from file_search import *
from pdf_util import * 
from vector_store_util import *
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', 't', 'yes', 'y', '1', 'on')
    return bool(value)

def get_final_list(resume_list:list)-> list:
  load_dotenv()
  concatPdf = os.getenv("concatPdf")
  finalpdf_list = []
  logging.info(f"concat pdf  : {concatPdf} {type(concatPdf)}")
  if parse_bool(concatPdf) == True:
    logging.info("concatenating pdf into concat_pdf")
    concat_pdf =concatenate_pdfs(resume_list)
    finalpdf_list.append(concat_pdf)
  else:
    logging.info(f"resume list  - {resume_list}")
    finalpdf_list = list(resume_list)
  logging.info(f"total file list - {len(finalpdf_list)}")
  return finalpdf_list 
      

def resume_search(resume1,resume2,prompt,chat_history):
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
    logging.info(f"instruction :  {instructions}")
    assistant_message = None
    assistant_output,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    result = "\n".join(assistant_output)
    logging.info(f"chatbot answering")
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": result})
     # clearing the prompt 
    cleared_prompt = ""
    return result ,assistant,thread,chat_history,cleared_prompt
  
def resume_search_cont(prompt : str,assistant_message : str,assistant : object,thread : object ,chat_history : object):
    logging.info("resume_search_cont prompt - 50 chars {prompt[0:50]}")
    result = None
    load_dotenv()
    vector_store_str = os.getenv("vector_store_resume")
    store_len,store_id,vector_store = search_vector_store(vector_store_str)
    logging.info(f"store_len {store_len} for {vector_store_str}")
    if  store_len == 0 :
    # check if store exists , if not skip creation
       logging.info(f"search error, vector store : {vector_store_str} not found")
    else :
      assistant_output =search_v2_cont(prompt,assistant_message,assistant,thread) 
      result = "\n".join(assistant_output)
    
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": result})
    # clearing the prompt 
    cleared_prompt = ""
    return result ,assistant,thread,chat_history,cleared_prompt

  
def format_resume_name(candidate_name):
  resume_name = candidate_name
  resume_name = resume_name.replace(" ","_")
  resume_name = resume_name + ".pdf"
  return resume_name
