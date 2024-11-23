def create_name_thumbnail(full_name, output_path=None):
    """
    Create a thumbnail with initials and full name
    Args:
        full_name (str): Full name of the person (e.g., 'Tanmay Patil')
        output_path (str, optional): Path to save the PNG file. 
                                   If None, uses the name to generate path
    Returns:
        str: Path to the generated PNG file
    """
    import cairosvg
    
    # Get initials from the name
    initials = ''.join(word[0].upper() for word in full_name.split())
    
    # If output_path is not provided, create one from the name
    if output_path is None:
        output_path = f"{full_name.replace(' ', '_')}_thumbnail.png"
        
    print(f' output path {output_path}')
    
    # Create SVG content
    svg_content = f'''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
        <!-- Background -->
        <rect width="800" height="800" fill="#ffffff"/>
        <!-- Blue border on left -->
        <rect x="0" y="0" width="64" height="800" fill="#2563eb"/>
        <!-- Initials -->
        <text x="432" y="400" 
              font-family="Arial, sans-serif" 
              font-size="280" 
              font-weight="bold"
              fill="#1e293b" 
              text-anchor="middle" 
              dominant-baseline="middle">{initials}</text>
        <!-- Full name -->
        <text x="432" y="600" 
              font-family="Arial, sans-serif" 
              font-size="80" 
              fill="#64748b" 
              text-anchor="middle" 
              dominant-baseline="middle">{full_name}</text>
    </svg>
    '''
    
    # Convert SVG to PNG
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'),
                     write_to=output_path,
                     output_width=800,
                     output_height=800)
    
    return output_path

# Example usage with Gradio
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