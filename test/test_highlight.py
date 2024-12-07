from highlight import * 

def test_highlight1(): 
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_exact_match.pdf"
    search_text = "A seasoned Engineering Director with 25 years"  
    highlight_text(pdf_path, search_text, output_path, exact_match=True)
    

def test_highlight21(): 
    print('running test_highlight2')
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_multi_match.pdf"
    search_text = '''A seasoned Engineering Director with 25 years of comprehensive experience in the software industry,
specializing in banking products for corporate clients. Proven track record in
    '''
    highlight_text(pdf_path, search_text, output_path, exact_match=True)

    
