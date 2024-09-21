import os
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io
from dotenv import load_dotenv
import file_search

# 1. search for text inside pdf 
# 2. annotate text create another pdf 
# 3. convert output into image
def pdf_search_annotate(pdf_file,search_text):
    search_annotate(pdf_file,search_text)
    output_file="highlighted_output.pdf"
    annotated = pdf_to_image_task(output_file)
    return annotated
    
# pdf upload task and convert to image
def pdf_to_image_task(pdf_file):
    # check if pdf file is provided
    if not pdf_file:
         raise ValueError("No pdf file provided , please upload the same")
    # Open the PDF from the uploaded file
    doc = fitz.open(pdf_file)
    images = []
    
    # Iterate through all the pages and convert them to images
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        # Append the image to the list
        images.append(img)
    return images 

# search & annotate pdf
def search_annotate(pdf_file,search_text):
  doc = fitz.open(pdf_file)
  print(f"search text {search_text}")
  for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    # Search for text and highlight
    text_instances = page.search_for(search_text)
    for inst in text_instances:
      print("found instance of search_text")
      highlight = page.add_highlight_annot(inst)
  # Save the document with highlights
  doc.save("highlighted_output.pdf")
  doc.close() 
  return doc

# Compare resumes
# 1.upload both resumes to vector store
# 2.run query 
# 3.get output 
def compare_resume(resume1,resume2,search_query):
    load_dotenv()
    vector_store_name = os.getenv("resume_compare")
    print(f"vector store name {vector_store_name}")
    file_list = [resume1,resume2]
    file_search.add_files(vector_store_name,file_list)
    return None

