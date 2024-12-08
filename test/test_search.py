from ResumeModel import ResumeModel
from format_util import * 
from resume_util import *
from vector_store_util import *
import os,openai 
from dotenv import load_dotenv
from file_search import *
from file_id_name import * 

load_dotenv()
key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=key)

def test_search1():
    delete_vector_store_files('resume_compare')
    resume1 = 'Arjun_Patel.pdf'
    resume2 = 'Suraj_Kumar.pdf'
    prompt = "Between Arjun Patel and Suraj Kumar looking at there resume's who is more suitable for handling stock market operations"
    assistant_output = resume_search(resume1,resume2,prompt)
    print(assistant_output)
    
def test_search2():
    delete_vector_store_files('resume_compare')
    resume1 = 'Arjun_Patel.pdf'
    resume2 = 'Suraj_Kumar.pdf'
    prompt = "Is Suraj Kumar competent for  handling stock market operations"
    assistant_output = resume_search(resume1,resume2,prompt)
    print(assistant_output)
    
def test_delete_files():
    delete_vector_store_files('resume_compare')
    
def test_list_vectorfiles():
    vector_store_files = client.beta.vector_stores.files.list(
    vector_store_id="vs_My7GdUMQ9huHOJlZcREd6529")
    print(vector_store_files)
    for file in vector_store_files:
        print(file.id)
        vector_store_file = client.beta.vector_stores.files.retrieve(
        vector_store_id="vs_My7GdUMQ9huHOJlZcREd6529",
        file_id=file.id )
        print(vector_store_file.status)
        print(vector_store_file.last_error)
        
def test_getinst():
    inst_id = 'readall_pdf'
    ins_text = get_instruction_useid(inst_id)
    assert ins_text != None
    print(ins_text)
    
    
        
def test_against_allfiles():
    file_upload_list = ['Rahul_Sharma.pdf','Rajesh_Kumar.pdf','Rahul_Mehta.pdf','Arjun_Patel.pdf']
    # search vector store first.
    _,store_id,vector_store = search_vector_store("resume_compare")
    # delete all files first from vector store
    delete_vector_store_files('resume_compare')
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all resumes available , which candidate ( provide name) is more suitable as a engineering manager for software engineering'
    # add files to vector store
    add_files_instore(vector_store,file_upload_list)
    assistant_message = None
    # query 
    assistant_output,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)

def test_engg_manager():
    _,store_id,vector_store = search_vector_store("resume_compare")
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all candidates , who has the more experience as a software engineering manager as per there resume . consider work experience , teams size managed'
    assistant_message = None
    # query 
    assistant_output,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)
    
def test_product_manager():
    _,store_id,vector_store = search_vector_store("resume_compare")
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'Amongst all candidates based on their resume , and experience who can play a role of product manager for core banking'
    assistant_message = None
    # query 
    assistant_output,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)

def test_against_allfiles_annotate():
    file_upload_list = ['Anjali_Kapoor.pdf','Arjun_Patel.pdf','Rajesh_Kumar.pdf']
    # search vector store first.
    _,store_id,vector_store = search_vector_store("resume_compare")
    # delete all files first from vector store
    delete_vector_store_files('resume_compare')
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all resumes available , which candidate ( provide name) is more suitable as a engineering manager for software engineering'
    # add files to vector store
    add_files_instore(vector_store,file_upload_list)
    assistant_message = None
    # query 
    assistant_output,annotations,found_text,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)
    print(f'Annotation : {annotations}')
    print(f'found_text  : {found_text}')

def test_against_noupload_annotate():
    # search vector store first.
    _,store_id,vector_store = search_vector_store("resume_compare")
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all resumes available, which candidate ( provide name) is more suitable as a engineering manager for software engineering considering team management and software skills'
    assistant_message = None
    # query 
    assistant_output,annotations,found_text,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)
    print(f'Annotation : {annotations}')
    print(f'found_text  : {found_text}')
    if annotations:
        fields_dict = find_selected_resume(annotations)
        print( f"fields_dict {fields_dict}")
    
def test_against_noupload1_annotate():
    # search vector store first.
    _,store_id,vector_store = search_vector_store("resume_compare")
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'Does Rajesh Kumar as per his resume has expertise in software engineering management'
    assistant_message = None
    # query 
    assistant_output,annotations,found_text,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)
    print(f'Annotation : {pretty_print_pydantic(annotations)}')
    final_annotations = []
    print(f'found_text  : {found_text}')

def test_against_allfiles_chunksize400():
    """test with changing file chunksize to 400  
    """
    file_upload_list = ['Anjali_Kapoor.pdf','Arjun_Patel.pdf','Rajesh_Kumar.pdf']
    # search vector store first.
    _,store_id,vector_store = search_vector_store("resume_compare")
    # delete all files first from vector store
    delete_vector_store_files('resume_compare')
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all resumes available , which candidate ( provide name) is more suitable as a engineering manager for software engineering'
    # add files to vector store , change chunksize to 400 from 800
    add_files_instore(vector_store,file_upload_list,max_chunk_size_tokens=400,chunk_overlap_tokens=200)
    assistant_message = None
    # query 
    assistant_output,annotations,found_text,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)
    print(f'Annotation : {annotations}')
    print(f'found_text  : {found_text}')

def test_against_allfiles_chunksize600():
    """test with changing file chunksize to 400  
    """
    file_upload_list = ['Anjali_Kapoor.pdf','Arjun_Patel.pdf','Rajesh_Kumar.pdf']
    # search vector store first.
    _,store_id,vector_store = search_vector_store("resume_compare")
    # delete all files first from vector store
    delete_vector_store_files('resume_compare')
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all resumes available , which candidate ( provide name) is more suitable as a engineering manager for software engineering'
    # add files to vector store , change chunksize to 600 from 800
    add_files_instore(vector_store,file_upload_list,max_chunk_size_tokens=600,chunk_overlap_tokens=300)
    assistant_message = None
    # query 
    assistant_output,annotations,found_text,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)
    print(f'Annotation : {annotations}')
    print(f'found_text  : {found_text}')
    
def test_extract_filename():
    file_dict = {'end_index': 726, 'file_citation': {'file_id': 'file-CzdfR52iCB2531GHBm992P'},
                 'start_index': 714, 'text': '【4:0†source】', 'type': 'file_citation'}
    file_id = file_dict['file_citation']['file_id']
    print(file_id)

def test_get_pdf_name():
    pdf_name =get_file_name_useid("file-CzdfR52iCB2531GHBm992P")
    print(f"pdf name : {pdf_name}")
    assert(pdf_name == 'Rajesh_Kumar.pdf')
    






   