from ResumeModel import ResumeModel
from format_util import * 
from resume_util import *

def test_search1():
    resume1 = 'Arjun_Patel.pdf'
    resume2 = 'Suraj_Kumar.pdf'
    prompt = 'Between Arjun Patel and Suraj Kumar who is more suitable for handling stock market operations'
    assistant_output = resume_search(resume1,resume2,prompt)
    print(assistant_output)