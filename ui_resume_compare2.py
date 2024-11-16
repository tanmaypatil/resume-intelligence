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

with gr.Blocks() as demo:
    assistant = gr.State()
    thread = gr.State()
    with gr.Row(equal_height=False):
        pdf_resume1 = gr.File(file_types=['.pdf'], label="Upload resume in PDF",scale=2)
        btn = gr.Button(value="Show resume", elem_id="small-btn1",scale=0)
        output_gallery1 = gr.Gallery(type="pil", label="Resume 1",elem_id="resume-gallery",scale=2)
    with gr.Row(equal_height=False):
        pdf_resume2 = gr.File(file_types=['.pdf'], label="Upload PDF",scale=2)
        btn2 = gr.Button(value="Show resume", elem_id="small-btn2",scale=0)
        output_gallery2 = gr.Gallery(type="pil", label="Resume 2",elem_id="resume-gallery2",scale=2)
    with gr.Row(equal_height=False):
        prompt = gr.Textbox(
            label="prompt",
            info="Enter search query",
            lines=3,
            value=" Between Rajesh kumar and Rahul Sharma who is more suitable to work as a engineering manager ",
        )
        ans = gr.Textbox(
            label="Search results",
            info="Search result of resume search",
            lines=3,
            value="",
        )
    with gr.Row(equal_height=False):
        btn3 = gr.Button(value="query", elem_id="query",scale=0)
        btn4 = gr.Button(value="submit", elem_id="submit",scale=0)
   
    btn.click(fn=convert_image, inputs=pdf_resume1, outputs=output_gallery1)
    btn2.click(fn=convert_image, inputs=pdf_resume2, outputs=output_gallery2)
    btn3.click(fn=resume_search, inputs=[pdf_resume1,pdf_resume2,prompt], outputs=[ans,assistant,thread])
    btn4.click(fn=resume_search_cont, inputs=[prompt,ans,assistant,thread], outputs=[ans,assistant,thread])

demo.launch()
