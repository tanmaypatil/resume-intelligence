
import json 
def get_file_name_useid(file_id):
    with open('.\\system_config\\file_ids.json') as file:
        file_arr = json.load(file)
    files = [item for item in file_arr if item["file_id"] == file_id]
    assert len(files) == 1
    pdf_name = files[0]['pdf_name']
    
    return pdf_name
