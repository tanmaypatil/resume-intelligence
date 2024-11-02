import gradio as gr
import json
from generate_resume_structured import *
from format_util import * 
from render_resume import *
from pdf_util import *
import logging
from PIL import Image
from PIL import Image, ImageDraw
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




def generate_resume_json(input_prompt):
      """Function to generate a resume in json format"""
      resume_json = generate_resume(input_prompt)
      if isinstance(resume_json, str):
        try:
            # Try to parse if it's a JSON string
          parsed_json = json.loads(resume_json)
          final_json = json.dumps(parsed_json, indent=2)
        except json.JSONDecodeError:
            # If it's just a regular string, convert it to JSON
            final_json = json.dumps({"text": resume_json}, indent=2)
      else:
         # If it's already a dictionary/object
         final_json = json.dumps(resume_json, indent=2)
    
      return final_json
  

  
def generate_resume_pdf(input_prompt):
      """Function to generate a resume in pdf format"""
      logging.info('generate_resume_pdf ')
      resume_json = generate_resume(input_prompt)
      parsed_json = resume_json
      
      if isinstance(resume_json, str):
        logging.info('resume_json is string ')
        try:
            # Try to parse if it's a JSON string
          parsed_json = json.loads(resume_json)
        except json.JSONDecodeError:
            # If it's just a regular string, convert it to JSON
            final_json = json.dumps({"text": resume_json}, indent=2)
            parsed_json = json.loads(final_json)
    
      contact_info = extract_personal_details(parsed_json)
      logging.info(f'generate_Resume_pdf {contact_info}')
      render_resume_pdf("sample_resume.pdf",contact_info)
      images= pdf_to_image_task("sample_resume.pdf")
      return images
    
def get_default_prompt():
      with open('.\\prompts_results\\prompt_dict.json') as file:
        json_data = json.load(file)
    
      if json_data is not None:
        default_prompt = json_data[0]['prompt']
        logging.info(f'Default prompt {default_prompt}')
      return default_prompt
        

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("### Give a promot to generate resume as per instruction")
    prompt = get_default_prompt()
    
    with gr.Row():
        # Input text area for JSON
        input = gr.TextArea(
            label="Enter candidates profile",
            lines=10,
            value=prompt
        )
        
        # Formatted output display
        json_output = gr.Code(
            label="Generated resume in JSON",
            language="json"
        )
    with gr.Row():
        resume_output = gr.Gallery(type="pil", label="Resume")
    with gr.Row():
        # Generate resume in JSON
        resume_json_button = gr.Button("Generate resume in JSON")
        # show resume in pdf
        resume_button = gr.Button("show resume in pdf")
        

    resume_json_button.click(
        fn=generate_resume_json,
        inputs=[input],
        outputs=[json_output]
    )
      
    resume_button.click(
        fn=generate_resume_pdf,
        inputs=[input],
        outputs=[resume_output]
    )

    gr.Markdown("""
    ### Usage Instructions:
    1. Enter or paste candidate career short description
    2. Click 'Generate resume in JSON' to see the formatted output
    3. Click 'Show resume in pdf' to see the pdf
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()