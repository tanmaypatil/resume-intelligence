import gradio as gr
import json
from generate_resume_structured import *



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
    

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("### Generate resume as per instruction")
    
    with gr.Row():
        # Input text area for JSON
        input = gr.TextArea(
            label="Enter candidates profile",
            lines=10
        )
        
        # Formatted output display
        json_output = gr.Code(
            label="Generated JSON",
            language="json"
        )
    
    # Update button
    format_button = gr.Button("Generate resume")
    format_button.click(
        fn=generate_resume_json,
        inputs=[input],
        outputs=[json_output]
    )

    gr.Markdown("""
    ### Usage Instructions:
    1. Enter or paste candidate career short description
    2. Click 'Generate resume' to see the formatted output
    3. The output will show proper indentation and formatting
    4. Invalid JSON will show an error message
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()