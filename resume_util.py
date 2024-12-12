from dotenv import load_dotenv
import os
from instructions import *
from file_search import *
from pdf_util import * 
from vector_store_util import *
import logging
import cairosvg
import gradio as gr
from file_id_name import * 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', 't', 'yes', 'y', '1', 'on')
    return bool(value)

def get_final_list(resume_list:list)-> list:
  load_dotenv(override=True)
  concat_pdf = os.getenv("CONCAT_PDF")
  finalpdf_list = []
  logging.info(f"concat pdf  : {concat_pdf} {type(concat_pdf)}")
  logging.info(f"concat pdf  : {concat_pdf} {type(concat_pdf)}")
  if parse_bool(concat_pdf) == True:
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

def get_text(item):
    if isinstance(item, list):
        return ", ".join(str(x) for x in item)
    elif isinstance(item, BaseModel):  # For FileCitationAnnotation objects
        return pformat(item.model_dump(), indent=2, width=120)
    else:
        return str(item)
  
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
      assistant_output,annotations,found_text,assistant,thread =search_v2_cont(prompt,assistant_message,assistant,thread) 
      result = "\n".join(get_text(item) for item in assistant_output)
  
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": result})
    # clearing the prompt 
    cleared_prompt = ""
    return result ,assistant,thread,chat_history,cleared_prompt,found_text,annotations
  
def find_selected_resume(annotations : list)->str : 
  file_name = None
  file_arr = []
  for anno in annotations:
    if isinstance(anno,BaseModel):
       anno_dict = anno.model_dump()  
       file_id = anno_dict['file_citation']['file_id'] 
       logging.info(f"annotated file_id  {file_id}") 
       file_name = get_file_name_useid(file_id)
       logging.info(f"post lookup selected file_name  {file_name}")
       file_arr.append(file_name)
  if(len(file_arr) > 0 ):
    file_name = file_arr[0]     
  logging.info(f"final selected file_name  {file_name}")
  return file_name

def resume_search_store(prompt,chat_history):
    logging.info(f"resume search complete store :{prompt}")
    result = ""
    # get vector store id 
    load_dotenv()
    vector_store_str = os.getenv("vector_store_resume")
    # check if store exists , if not skip creation 
    store_len,store_id,vector_store = search_vector_store(vector_store_str)
    logging.info(f"store_len {store_len} for {vector_store_str}")
    if store_len == 0:
      gr.Error("vector store :'resume_compare' does not exist ")
      logging.error(f"vector store :'resume_compare' does not exist")
      return None,None,None,None,None
    else :
      logging.info(f'vector store id {store_id}')
    # get the instructions to assistant 
    instructions , inst_file_id = get_instructions()
    logging.info(f"instruction file id  {inst_file_id}")
    logging.info(f"instruction :  {instructions}")
    assistant_message = None
    assistant_output,annotations , found_text ,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    result = "\n".join(assistant_output)
    logging.info(f"chatbot answering")
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": result})
     # clearing the prompt 
    cleared_prompt = ""
    return result ,assistant,thread,chat_history,cleared_prompt,found_text,annotations


  
def format_resume_name(candidate_name):
  resume_name = candidate_name
  resume_name = resume_name.replace(" ","_")
  resume_name = resume_name + ".pdf"
  return resume_name

def create_name_thumbnail(full_name, output_path=None):
    """
    Create a thumbnail with initials and full name
    Args:
        full_name (str): Full name of the person (e.g., 'Tanmay Patil')
        output_path (str, optional): Path to save the PNG file. 
                                   If None, uses the name to generate path
    Returns:
        str: Path to the generated PNG file
    """
    
    # Get initials from the name
    initials = ''.join(word[0].upper() for word in full_name.split())
    
    # If output_path is not provided, create one from the name
    if output_path is None:
        output_path = f"{full_name.replace(' ', '_')}_thumbnail.png"
    else:
       output_path = f"{output_path}\\{full_name.replace(' ', '_')}_thumbnail.png"
        
    print(f' output path {output_path}')
    
    # Create SVG content
    svg_content = f'''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
        <!-- Background -->
        <rect width="800" height="800" fill="#ffffff"/>
        <!-- Blue border on left -->
        <rect x="0" y="0" width="64" height="800" fill="#2563eb"/>
        <!-- Initials -->
        <text x="432" y="400" 
              font-family="Arial, sans-serif" 
              font-size="280" 
              font-weight="bold"
              fill="#1e293b" 
              text-anchor="middle" 
              dominant-baseline="middle">{initials}</text>
        <!-- Full name -->
        <text x="432" y="600" 
              font-family="Arial, sans-serif" 
              font-size="80" 
              fill="#64748b" 
              text-anchor="middle" 
              dominant-baseline="middle">{full_name}</text>
    </svg>
    '''
    
    # Convert SVG to PNG
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'),
                     write_to=output_path,
                     output_width=800,
                     output_height=800)
    
    return output_path

