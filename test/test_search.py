from ResumeModel import ResumeModel
from format_util import * 
from resume_util import *
from vector_store_util import * 

def test_search1():
    delete_vector_store_files('resume_compare')
    resume1 = 'Arjun_Patel.pdf'
    resume2 = 'Suraj_Kumar.pdf'
    prompt = "Between Arjun Patel and Suraj Kumar looking at there resume's who is more suitable for handling stock market operations"
    assistant_output = resume_search(resume1,resume2,prompt)
    print(assistant_output)
    
def test_search2():
    delete_vector_store_files('resume_compare')
    resume1 = 'Arjun_Patel.pdf'
    resume2 = 'Suraj_Kumar.pdf'
    prompt = "Is Suraj Kumar competent for  handling stock market operations"
    assistant_output = resume_search(resume1,resume2,prompt)
    print(assistant_output)