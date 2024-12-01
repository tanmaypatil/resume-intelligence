import gradio as gr
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io
import logging
from file_util import *
from vector_store_util import *
from resume_util import * 
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

def search_resume_store(prompt,chatbot):
  return resume_search_store(prompt,chatbot)    
  

def clean_docs(image_gallery :list ):
  if image_gallery:
    logging.info(f'cleaning docs from resume_compare , inside resume folder doc count {len(image_gallery)}')
  gr.Info("cleaning docs from file store")
  files_deleted = delete_vector_store_files('resume_compare')
  delete_files('.\\resumes','*',False)
  logging.info(f'cleaning up - complete , files deleted #{files_deleted}')
  gr.Info(f'cleaning up - complete , files deleted #{files_deleted}')
  return [],[]

  
def upload_all(image_gallery : list):
  try :
    logging.info('uploading all docs to resume_compare')
    store_len,_,store_obj = search_vector_store('resume_compare')
    copy_folder_contents('.\\resumes_gen','.\\resumes')
    resume_list = list_files_with_extension('.\\resumes','pdf')
    gr.Info(f'Uploading files to file store #{len(resume_list)}')
    add_files_instore(store_obj,resume_list)
    logging.info('uploaded all docs to resume_compare')
    list = list_files_with_extension(".\\resumes","png")
    list_gallery = [ ( '.\\resumes\\' + l,'.\\resumes\\' + l.removesuffix("_thumbnail.png") + '.pdf') for l in list ]
    return list_gallery
  except Exception as e:
    logging.error(f"An error occurred: {str(e)}", err=True)
    gr.Warning('Files did not get uploaded to file store')
    return []

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

    
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Smart Resume Review")
    assistant = gr.State()
    thread = gr.State()
    assistant_message = gr.State()
   
    with gr.Row(equal_height=False):
      # get list of the thumbnails
      list = list_files_with_extension(".\\resumes","png")
      list_gallery = [ ( '.\\resumes\\' + l,'.\\resumes\\' + l.removesuffix("_thumbnail.png") + '.pdf') for l in list ]

      gallery = gr.Gallery( value = list_gallery,height=150,rows=1,columns=7,selected_index=0,label="Resumes",interactive=False,elem_id="resume_thumbnail" )    
      resume = gr.Gallery(label='Selected Resume')
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
            value="  ",
            interactive=True
        )
      chatbot = gr.Chatbot(type="messages", label="Resume intelligence")
    with gr.Row():
      query = gr.Button(value="query", variant='primary',elem_id="query",scale=0)
      upd_all = gr.Button("upload all",variant='secondary',elem_id="upd_all",scale=0)
      clr_all = gr.Button("clear all",variant='secondary',elem_id="clr_all",scale=0)
      
    
    # hook event handler to display resume   
    gallery.select(on_select, gallery, resume)
    # event handler for uploading documents
    upd_all.click(fn=upload_all,inputs=[gallery],outputs=[gallery])
      # event handler for clearing documents
    clr_all.click(fn=clean_docs,inputs=[gallery],outputs=[gallery,resume])
    # event handler for querying resume file store
    query.click(fn=search_resume_store,inputs=[prompt,chatbot],outputs=[assistant_message,assistant,thread,chatbot,prompt])
    
    

demo.launch()