import io
import gradio as gr
import fitz  # PyMuPDF for PDF handling
from PIL import Image
from resume_util import *

def convert_image(pdf_file):
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

with gr.Blocks() as demo:
    with gr.Row():
      gallery = []
      resume_list = ['Rahul_Sharma.pdf','Rahul_Mehta.pdf','Rajesh_Kumar.pdf'] 
      for resume in resume_list:
         label = resume.strip('.pdf')
         img_arr = convert_image(resume) 
         output_gallery1 = gr.Gallery(value=img_arr,type="pil", label=label,elem_id="resume-gallery",height=50,scale=0,preview=True)
         gallery.append(output_gallery1)
    
demo.launch()
