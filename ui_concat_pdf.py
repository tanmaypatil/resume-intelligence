from concurrent.futures import ThreadPoolExecutor, as_completed
import fitz  # PyMuPDF for PDF handling
import gradio as gr
from PIL import Image
import io
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# pdf to image conversion task.
def pdf_to_image_task(pdf_file):
    # check if pdf file is provided
    #if not pdf_file:
    # raise ValueError("No pdf file provided , please upload the same")
    
    # Open the PDF from the uploaded file
    logging.info(f"pdf_to_image_task {pdf_file}")
    doc = fitz.open(pdf_file)
    images = []
    
    # Iterate through all the pages and convert them to images
    for page_num in range(len(doc)):
        logging.info(f"pdf_to_image_task converting {page_num} to image ")
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        # Append the image to the list
        images.append(img)
    return images 

def concatenate_pdfs(pdf1,pdf2):
    output_file = "pdf_concat.pdf"
    pdf_files = [ pdf1,pdf2]
    # Create a new PDF document
    output_pdf = fitz.open()

    for pdf_file in pdf_files:
        # Open the current PDF
        pdf_document = fitz.open(pdf_file)

        # Insert the entire PDF into the output PDF
        output_pdf.insert_pdf(pdf_document)

        # Close the current PDF
        pdf_document.close()

    # Save the concatenated PDF to a file
    output_pdf.save(output_file)
    #output_pdf.close()
    # convert to image 
    image = pdf_to_image_task(output_file)
    return image

# Create the Gradio interface for concatenating pdf
pdf_input1 = gr.File(file_types=['.pdf'], label="Upload PDF 1")
pdf_input2 = gr.File(file_types=['.pdf'], label="Upload PDF 2")
  
output_gallery = gr.Gallery(type="pil", label="PDF concatenated Pages")
output = gr.Textbox(
            label="result",
            info="output of search",
            lines=3,
            value="output will appear here ",
        )

interface = gr.Interface(
    fn=concatenate_pdfs,  # Function to concatenate and display the PDF
    inputs=[pdf_input1,pdf_input2],  # Input widget to upload the PDF
    outputs=[output_gallery],  # Output as images
    title="Concatenate 2 pdfs",
    description="Upload 2 PDF file(s) and concatenate same and display pages as images."
)

# Launch the interface
interface.launch()
