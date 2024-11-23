from ResumeModel import ResumeModel
from format_util import * 
from resume_util import *
from vector_store_util import *
import os,openai 
from dotenv import load_dotenv

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

def test_withoutdelete():
    _,store_id,vector_store = search_vector_store("resume_compare")
    # get instructions
    instructions,_ = get_instruction_useid('readall_pdf')
    # set the prompt
    prompt = 'amongst all candidates , who has the more experience as a software engineering manager as per there resume . consider work experience , teams size managed'
    assistant_message = None
    # query 
    assistant_output,assistant,thread = search_v2([store_id],prompt,instructions,assistant_message)
    print(assistant_output)

   