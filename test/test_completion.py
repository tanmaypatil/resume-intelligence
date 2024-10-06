
from completion import generate_completion
from file_search import *
from pdf_totext import extract_text_from_pdf
from dotenv import load_dotenv
from vector_store_util import * 
import os
from claudette import * 

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_KEY")



def test_completion():
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is a LLM?"}
  ]
  completion = generate_completion(messages)
  print("Generated Completion:")
  print(completion)
  
def test_pdfextract():
  pdf_file_path = 'Tanmay_patil_finastra_Resume.pdf'  # Replace with your PDF file path
  start_page = 0  # Start page index (0-based)
  end_page = 1    # End page index (0-based)

  extracted_text = extract_text_from_pdf(pdf_file_path, start_page, end_page)
  print(extracted_text)
  
def test_filesearch():
  store_name = 'resume_store'
  file_list = ['files\\Tanmay_patil_finastra_Resume.pdf']
  add_files(store_name,file_list)
  s = list_stores()
  print(s)
  
def test_liststore():
  s = list_stores()
  print(s)
  
def test_searchstore():
  search_text = 'what was Tanmay Patils work in API governance'
  # store_id is retrieved 
  store_id = 'vs_Rxi64D4Z3ntBfcJDqrPPhgpP'
  search([store_id],search_text)

def test_env():
      print('123')
      v_id = os.getenv('vector_store_id')
      print(v_id)
      assert v_id != None

def test_create_store():
      store_name = 'resume-intelligence'
      v_store = create_vector_store(store_name)
      print(v_store.id)
      assert v_store.id != None
      
def test_list_store():
      store_name = 'resume-intelligence'
      store_len,_ = search_vector_store(store_name)
      assert store_len == 1

def test_claude():
      assert models != None
      print(models[1])
      
      
      
      
      
      
  
  