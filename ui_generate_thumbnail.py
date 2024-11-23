from resume_util import *
import gradio as gr

def generate_thumbnail(name):
    if not name:
        return None
    output_path = create_name_thumbnail(name)
    return output_path

# Create Gradio interface
demo = gr.Interface(
    fn=generate_thumbnail,
    inputs=gr.Textbox(label="Enter Full Name", placeholder="e.g., Tanmay Patil"),
    outputs=gr.Image(label="Generated Thumbnail", height=100, width=100),  # Smaller display size
    title="Name Thumbnail Generator",
    description="Generate a professional thumbnail with initials and full name"
)

if __name__ == "__main__":
    demo.launch()