from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF handling
import gradio as gr
from PIL import Image
import io
import os
from file_search import search,add_files
from pdf_util import * 
from vector_store_util import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compare_resumes(resume1,resume2,prompt):
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
    concat_pdf =concatenate_pdfs([resume1,resume2])
    logging.info(f"concatenated resume {concat_pdf}")
    file_list = [concat_pdf]
    # index file into vector store
    logging.info(f"index into vector store {file_list} ")
    store_id = add_files_instore(vector_store,file_list)
    logging.info(f"post creating index  {store_id}")
    # search for comparative analysis
    assistant_output = search([store_id],prompt)
    result = "\n".join(assistant_output)
    # convert resume 1 and resume 2 for displaying as image 
    image_gallery1 = pdf_to_image_task(resume1)
    image_gallery2 = pdf_to_image_task(resume2)
    return  image_gallery1 , image_gallery2 ,result 

# pdf upload task
def pdf_to_image_task(pdf_file):
    # check if pdf file is provided
    if not pdf_file:
         raise ValueError("No pdf file provided , please upload the same")
    # Open the PDF from the uploaded file
    doc = fitz.open(pdf_file.name)
    images = []
    
    # Iterate through all the pages and convert them to images
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        # Append the image to the list
        images.append(img)
    return images 

# Upload resume 1
pdf_resume1 = gr.File(file_types=['.pdf'], label="Upload PDF")
# Upload resume 2
pdf_resume2 = gr.File(file_types=['.pdf'], label="Upload PDF")

prompt = gr.Textbox(
            label="prompt",
            info="Enter search query",
            lines=3,
            value="Between Arti Patil and Tanmay Patil who has more experience in teaching a german language ",
        )
output_gallery1 = gr.Gallery(type="pil", label="Resume 1")
output_gallery2 = gr.Gallery(type="pil", label="Resume 2")
query_result = gr.Textbox(
            label="result",
            info="output of search",
            lines=3,
            value="output will appear here ",
        )

interface = gr.Interface(
    fn=compare_resumes,  # Function to process and compare resumes
    inputs=[pdf_resume1,pdf_resume2,prompt],  # Input widget to upload the PDF
    outputs=[output_gallery1,output_gallery2,query_result],  # Output as images amd result
    title="Resume intelligence",
    description="Upload 2 resume's in PDF and we will compare 2 resumes"
)

# Launch the interface
interface.launch()
