from format_util import * 

def test_json_list():
    with open('.\\prompts_results\\devops_engg.json') as file:
      json_data = json.load(file)
      assert json_data != None
      list_data = extract_personal_details(json_data)
      assert(len(list_data) == 3)