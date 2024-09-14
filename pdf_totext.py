import PyPDF2

def extract_text_from_pdf(pdf_file, start_page, end_page):
    pdf_path = f"files\\{pdf_file}"
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        
        # Get the number of pages in the PDF
        total_pages = len(reader.pages)
        
        # Validate the start and end pages
        if start_page < 0 or end_page > total_pages or start_page > end_page:
            raise ValueError("Invalid start or end page")

        # Initialize an empty string to store the extracted text
        extracted_text = ""

        # Loop through the specified range of pages
        for page_num in range(start_page, end_page + 1):
            page = reader.pages[page_num]
            extracted_text += page.extract_text()

        return extracted_text


