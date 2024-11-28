import gradio as gr
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io

from file_util import list_files_with_extension

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
    gallery = gr.Gallery(value = list_gallery,scale=0,height=60,rows=1,columns=7,selected_index=0,show_label=False
                         )
    resume = gr.Gallery(label='resume')
    statement = gr.Textbox()

    def on_select( evt : gr.SelectData,second):
        print(type(evt))
        print(f"value : {evt.value} , type : {type(evt.value)}")
        file_name = evt.value['caption']
        print(f"resume name {file_name}")
        file_with_path = file_name
        img_arr = convert_image(file_with_path)
        return img_arr

    gallery.select(on_select, gallery, resume)
    

demo.launch()