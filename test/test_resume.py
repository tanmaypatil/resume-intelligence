from ResumeModel import ResumeModel
from format_util import * 

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

