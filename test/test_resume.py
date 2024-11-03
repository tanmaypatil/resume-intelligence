from ResumeModel import ResumeModel
from format_util import * 
from resume_util import *

# {"experience" } - braces are important
# else json.loads does not work.
experience_str =''' 
  {"experience": [
    {
      "company": "Tech Innovators Inc.",
      "position": "Senior DevOps Engineer",
      "duration": "2018 - Present",
      "achievements": [
        "Led the transition to a cloud-native infrastructure, resulting in a 30% reduction in operational costs.",
        "Implemented Kubernetes for container orchestration, improving application deployment speed by 40%.",
        "Developed CI/CD pipelines that decreased software release cycles from bi-weekly to daily."
      ]
    },
    {
      "company": "Global Solutions Ltd.",
      "position": "DevOps Engineer",
      "duration": "2014 - 2018",
      "achievements": [
        "Managed cloud services across AWS, Azure, and GCP to support global operations.",
        "Automated infrastructure provisioning using Terraform, enhancing scalability and reliability.",
        "Collaborated with development teams to integrate DevOps practices, boosting productivity by 25%."
      ]
    }
  ] }
  '''

def test_json_list():
    with open('.\\prompts_results\\devops_engg.json') as file:
      json_data = json.load(file)
      assert json_data != None
      list_data,_,_,_,_ = extract_personal_details(json_data)
      assert(len(list_data) == 3)

def test_ResumeModel1():
    with open('.\\prompts_results\\devops_engg.json') as file:
      json_data = json.load(file)
      assert json_data != None
      r = ResumeModel(json_data)
      assert r.email != None 
      assert r.email == 'rahul.sharma@example.com'
      assert r.name == 'Rahul Sharma'

def test_resume_name():
    name = 'Alex kumar'
    formatted_name = format_resume_name(name)
    print(f"{formatted_name}")
    
def test_experience():
  exp = json.loads(experience_str)
  exp_arr = exp['experience']
  for e in exp_arr:
    ach_list =  e['achievements']
    print(f"type of ach_list {type(ach_list)}")
    str =  ("\n").join(ach_list) 
    print(str)      
    
def test_no_list_comprehension():
    list =  [ "str1", "str2"]
    str =  ("\n").join(list)    
    print(str)
    

