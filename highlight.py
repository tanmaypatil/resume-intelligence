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
def highlight_multiline_text_flexible(pdf_path, search_text, output_path, highlight_color=(1, 1, 0), max_line_distance=3):
    """
    Highlight multi-line text with flexible line spacing.
    
    Args:
        pdf_path (str): Path to input PDF file
        search_text (str): Multi-line text to search and highlight
        output_path (str): Path to save the highlighted PDF
        highlight_color (tuple): RGB color for highlighting (default: yellow)
        max_line_distance (int): Maximum number of blocks that can appear between matching lines
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Prepare the search text
    search_lines = [line.strip() for line in search_text.split('\n') if line.strip()]
    
    # Process each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        blocks = page.get_text("blocks")
        
        # Look for matches starting at each block
        for start_idx in range(len(blocks)):
            matches = []
            current_line_index = 0
            skip_count = 0
            
            # Try to match all lines starting from this block
            for block_idx in range(start_idx, min(len(blocks), start_idx + len(search_lines) + max_line_distance * (len(search_lines) - 1))):
                block_text = blocks[block_idx][4].strip()
                
                if search_lines[current_line_index] in block_text:
                    matches.append(blocks[block_idx])
                    current_line_index += 1
                    skip_count = 0
                    
                    if current_line_index >= len(search_lines):
                        # All lines matched - highlight them
                        for match_block in matches:
                            rect = fitz.Rect(match_block[:4])
                            highlight = page.add_highlight_annot(rect)
                            highlight.set_colors(stroke=highlight_color)
                            highlight.update()
                        break
                else:
                    skip_count += 1
                    if skip_count > max_line_distance:
                        break
    
    # Save the modified PDF
    pdf_document.save(output_path)
    pdf_document.close()

