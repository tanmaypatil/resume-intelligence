

from file_search import *
from pdf_totext import extract_text_from_pdf
from dotenv import load_dotenv
from vector_store_util import * 
import os
from claudette import * 
from instructions import *


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
      
def create_test_image():
    from PIL import Image
    import io

    # Create a small, valid PNG image
    img = Image.new('RGB', (50, 50), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def test_chat():
      print(models[1])
      img_bytes = create_test_image()
      load_dotenv()
      #print(f"api key {os.getenv('ANTHROPIC_KEY3')}")
      os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_KEY3")
      chat = Chat(models[1])
      query = "what is tanmay patils role in finastra"
      ans = chat([img_bytes,query])
      print(ans)
      
def test_env_model():
      load_dotenv()
      print(f"model == {os.getenv('model')}")
      
def test_env_instruction():
      with open("system_config\\instructions.txt",'r') as file:
        content = file.read()
        print(f"content == {content}")
        
def test_env_instruction2():
      load_dotenv()
      print(f' {os.getenv("CONCAT_PDF")}') 
      print(f" instruction_id - {os.getenv('instruction_id')} ")
      instruction_text,_ = get_instructions()
      print(f"first 20 chars : {instruction_text[0:20]}")

def test_del_vect_files():
      len_store = delete_vector_store_files('resume_compare')
      print(f'deleted {len_store} files from resume_compare')
      
def test_bool():
      flag = 'False'
      if bool(flag) == True:
        print('True')
      else :
        print('False')
      
      
     
      

      
      
      
      
      
  
  