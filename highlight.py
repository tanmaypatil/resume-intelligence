import fitz
import re

def highlight_text(pdf_path, search_text, output_path, highlight_color=(1, 1, 0), exact_match=False):
    """
    Highlight text in a PDF file.
    
    Args:
        pdf_path (str): Path to input PDF file
        search_text (str): Text to search and highlight
        output_path (str): Path to save the highlighted PDF
        highlight_color (tuple): RGB color for highlighting (default: yellow)
        exact_match (bool): Whether to search for exact matches only
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Compile search pattern
    if not exact_match:
        # Case-insensitive partial matching
        pattern = re.compile(re.escape(search_text), re.IGNORECASE)
    
    # Process each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        if exact_match:
            # Search for exact matches
            matches = page.search_for(search_text)
        else:
            # Search for partial matches using regular expressions
            words = page.get_text("words")
            matches = []
            
            for word in words:
                text = word[4]  # The actual text content
                if pattern.search(text):
                    # Create rectangle for highlighting
                    rect = fitz.Rect(word[0], word[1], word[2], word[3])
                    matches.append(rect)
        
        # Apply highlighting to all matches
        for match in matches:
            highlight = page.add_highlight_annot(match)
            highlight.set_colors(stroke=highlight_color)
            highlight.update()
    
    # Save the modified PDF
    pdf_document.save(output_path)
    pdf_document.close()

# Example usage with exact matching


# Example usage with partial matching
def example_partial_match():
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_partial_match.pdf"
    search_text = "A seasoned Engineering Director with 25 years"  
    
    # Using orange color for highlighting
    highlight_text(pdf_path, search_text, output_path, 
                  highlight_color=(1, 0.65, 0), 
                  exact_match=True)
