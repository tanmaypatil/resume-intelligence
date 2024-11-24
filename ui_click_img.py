import gradio as gr
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io

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
    gallery = gr.Gallery(value = [( "Tanmay_patil_thumbnail.png","Rahul_Mehta.pdf"),( "Andrej_Karpathy_thumbnail.png","Rahul_Sharma.pdf")],scale=0,height=60,rows=1,columns=2,selected_index=0
                         )
    resume = gr.Gallery(label='resume')
    statement = gr.Textbox()

    def on_select( evt : gr.SelectData,second):
        print(type(evt))
        print(f"value : {evt.value} , type : {type(evt.value)}")
        file_name = evt.value['caption']
        print(f"resume name {file_name}")
        img_arr = convert_image(file_name)
        return img_arr

    gallery.select(on_select, gallery, resume)
    

demo.launch()