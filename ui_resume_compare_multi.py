import gradio as gr
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io
import logging
from file_util import list_files_with_extension
from vector_store_util import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')


def clean_docs():
  logging.info('cleaning docs from resume_compare')
  delete_vector_store_files('resume_compare')
  
def upload_all():
    logging.info('uploading all docs to resume_compare')
    store_len,_,store_obj = search_vector_store('resume_compare')
      

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

# get list of the thumbnails
list = list_files_with_extension(".\\resumes","png")
list_gallery = [ ( '.\\resumes\\' + l,'.\\resumes\\' + l.removesuffix("_thumbnail.png") + '.pdf') for l in list ]
    
with gr.Blocks() as demo:
    with gr.Row(equal_height=False):
      gallery = gr.Gallery(value = list_gallery,height=150,rows=1,columns=7,selected_index=0,show_label=None )
      resume = gr.Gallery(label='resume')
      # handler to display resume 
      def on_select( evt : gr.SelectData,second):
        print(type(evt))
        print(f"value : {evt.value} , type : {type(evt.value)}")
        file_name = evt.value['caption']
        print(f"resume name {file_name}")
        file_with_path = file_name
        img_arr = convert_image(file_with_path)
        return img_arr
    with gr.Row(equal_height=False):
      prompt = gr.Textbox(
            label="prompt",
            info="Enter search query",
            lines=3,
            value=" Between Rajesh kumar and Rahul Sharma who is more suitable to work as a engineering manager ",
        )
      chatbot = gr.Chatbot(type="messages", label="Resume intelligence")
    with gr.Row():
      upd_all = gr.Button("upload all",variant='primary',elem_id="upd_all",scale=0)
      clr_all = gr.Button("clear all",variant='primary',elem_id="clr_all",scale=0)
    
    # hook event handler to display resume   
    gallery.select(on_select, gallery, resume)
    # event handler for clearing documents
    upd_all.click(fn=upload_all)
    clr_all.click(fn=clean_docs)
    
    

demo.launch()