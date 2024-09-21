from concurrent.futures import ThreadPoolExecutor, as_completed
import fitz  # PyMuPDF for PDF handling
import gradio as gr
import pdf_util

# Create the Gradio interface
pdf_input = gr.File(file_types=['.pdf'], label="Upload PDF")
prompt = gr.Textbox(
            label="prompt",
            info="Enter search query",
            lines=3,
            value="api governance.",
        )
output_gallery = gr.Gallery(type="pil", label="annotated pdf")

interface = gr.Interface(
    fn=pdf_util.pdf_search_annotate,  # Function to process and display the PDF
    inputs=[pdf_input,prompt],  # Input widget to upload the PDF
    outputs=[output_gallery],  # Output as images
    title="Resume intelligence",
    description="Upload a PDF file and annotate relevant sections ."
)

# Launch the interface
interface.launch()
