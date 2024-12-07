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
    
def test_highlight22(): 
    print('running test_highlight22')
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_multi_match.pdf"
    search_text = '''(anonymous)


Rajesh Kumar

rajesh.kumar@email.com'''
    search_text = search_text.lstrip('(anonymous)')
    print(f'search_text : {search_text}')
    highlight_text(pdf_path, search_text, output_path, exact_match=True)
    
def test_highlight23(): 
    print('running test_highlight22')
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_multi_match.pdf"
    search_text = '''
rajesh.kumar@email.com'''
    print(f'search_text : {search_text}')
    highlight_text(pdf_path=pdf_path, search_text=search_text, output_path=output_path, exact_match=True)
    
def test_highlight_multiline(): 
    print('running test_multiline')
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_multi_match.pdf"
    search_text = '''
Rajesh Kumar

rajesh.kumar@email.com'''

    print(f'search_text : {search_text}')
    highlight_multiline_text_flexible(pdf_path, search_text, output_path)

def test_highlight44(): 
    print('running test_highlight22')
    pdf_path = ".\\resumes\\Rajesh_Kumar.pdf"
    output_path = ".\\resumes_highlighted\\output_multi_match.pdf"
    search_text = '''(anonymous)


Rajesh Kumar

rajesh.kumar@email.com'''
    search_text = search_text.lstrip('(anonymous)')
    print(f'search_text : {search_text}')
    highlight_multiline_text_flexible(pdf_path, search_text, output_path)

    
